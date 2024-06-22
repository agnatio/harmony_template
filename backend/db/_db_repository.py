# this is reference from another project, will be deleted


# Assuming your db_models.py and db_init.py are properly set up
from typing import List
from sqlalchemy import update, desc
from sqlalchemy.orm import Session
from db.db_models import User as DBUser
from db.db_models import Instance as DBInstance
from db.db_models import UserDefaultInstance as DBUserDefaultInstance
from db.db_models import UserDefaultInstanceDetail as DBUserDefaultInstanceDetail
from db.db_models import SQLQueriesHistory, ChatGPTRequestsHistory
from db.db_init import SessionLocal
from schemas.pydantic_schemas import (
    SUserCreate,
    SInstanceCreate,
    SInstanceOut,
    SUserDefaultInstanceDetail,
)
from icecream import ic
from genpass_folder.genpass import EncryptionManager
from genpass_folder.crypto_fernet import secret_key
from datetime import datetime, timedelta

encryption_manager = EncryptionManager(secret_key)


class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(self, user: SUserCreate) -> DBUser:
        hashed_password = (
            user.hashed_password()
        )  # Assuming SUserCreate has a method to hash passwords
        db_user = DBUser(
            username=user.username, email=user.email, hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_username(self, username: str) -> DBUser:
        return self.db.query(DBUser).filter(DBUser.username == username).first()

    def get_user_by_id(self, id) -> DBUser:
        return self.db.query(DBUser).filter(DBUser.id == id).first()

    def update_user(self, user_id: int, user_data: SUserCreate) -> DBUser:
        db_user = self.get_user_by_id(user_id)
        if db_user:
            # Update user data in the database
            update_data = {
                DBUser.username: user_data.username,
                DBUser.email: user_data.email,
                DBUser.hashed_password: user_data.hashed_password(),  # Assuming this returns the hashed password
                DBUser.is_superuser: user_data.is_superuser,
            }
            self.db.execute(
                update(DBUser).where(DBUser.id == user_id).values(update_data)
            )
            self.db.commit()

            # Fetch and return the updated user from the database
            updated_user = self.get_user_by_id(user_id)
            return updated_user
        return None

    def delete_user(self, username: str):
        db_user = self.get_user_by_username(username)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()

    def delete_user_by_id(self, user_id: int):
        # Find the user by ID instead of username
        db_user = self.db.query(DBUser).filter(DBUser.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()

    def get_all_users(self) -> List[DBUser]:
        return self.db.query(DBUser).all()


class InstanceRepository:
    def __init__(self, db_session: Session, username: str):
        self.db = db_session
        self.username = username

    def _get_user_by_username(self):
        return self.db.query(DBUser).filter(DBUser.username == self.username).first()

    def create_instance(self, instance_data: SInstanceCreate) -> DBInstance:
        user = self._get_user_by_username()
        if not user:
            raise ValueError("User not found")

        encrypted_password = instance_data.encrypt_instance_password()

        # Use the provided value or default to the specified string if the value is None
        xdo_destination = instance_data.xdo_destination or "Harmony"
        xdm_destination = instance_data.xdm_destination or "Harmony"

        new_instance = DBInstance(
            url=str(instance_data.url),
            instance_user=instance_data.instance_user,
            instance_password=encrypted_password,
            owner_id=user.id,
            instance_nickname=instance_data.instance_nickname,
            stealth_mode=(
                instance_data.stealth_mode
                if instance_data.stealth_mode is not None
                else False
            ),
            xdo_destination=xdo_destination,
            xdm_destination=xdm_destination,
        )
        self.db.add(new_instance)
        self.db.commit()
        self.db.refresh(new_instance)
        return new_instance

    def set_default_instance(self, user_id: int, instance_id: int):
        # First, check if there's an existing default instance setting for this user
        default_setting = (
            self.db.query(DBUserDefaultInstance)
            .filter(DBUserDefaultInstance.user_id == user_id)
            .first()
        )

        if default_setting:
            # If there's an existing setting, update it with the new instance_id
            default_setting.default_instance_id = instance_id
        else:
            # If there's no existing setting, create a new one
            new_default_setting = DBUserDefaultInstance(
                user_id=user_id, default_instance_id=instance_id
            )
            self.db.add(new_default_setting)

        # Commit the changes to the database
        self.db.commit()

        # Optionally, return some information or confirmation
        return {"message": "Default instance updated successfully"}

    def is_default_instance(self, user_id: int, instance_id: int) -> bool:
        # Check if the given instance is set as the default for the given user
        default_instance = (
            self.db.query(DBUserDefaultInstance)
            .filter(
                DBUserDefaultInstance.user_id == user_id,
                DBUserDefaultInstance.default_instance_id == instance_id,
            )
            .first()
        )
        return default_instance is not None

    def remove_default_instance(self, user_id: int):
        # Remove the default instance setting for the given user
        default_instance = (
            self.db.query(DBUserDefaultInstance)
            .filter(DBUserDefaultInstance.user_id == user_id)
            .first()
        )
        if default_instance:
            self.db.delete(default_instance)
            self.db.commit()

    def delete_instance(self, instance_id: int):
        user = self._get_user_by_username()
        if not user:
            print("User not found")
            return False

        # Check if the instance being deleted is set as the default instance
        if self.is_default_instance(user.id, instance_id):
            self.remove_default_instance(user.id)  # Remove the default instance setting

        # Proceed to delete the instance itself
        instance = self.get_instance_by_id_and_username(instance_id)
        if instance:
            try:
                self.db.delete(instance)
                self.db.commit()
                print(f"Instance with ID {instance_id} successfully deleted.")
                return True
            except Exception as e:
                print(f"An error occurred while deleting the instance: {e}")
                self.db.rollback()
                return False
        else:
            print(
                f"Instance with ID {instance_id} not found or does not belong to user {self.username}."
            )
            return False

    def get_default_instance_id_for_user(self, user_id) -> int:
        default_setting = (
            self.db.query(DBUserDefaultInstance)
            .filter(DBUserDefaultInstance.user_id == user_id)
            .first()
        )
        if default_setting:
            # If there's a default setting, return the default_instance_id
            return default_setting.default_instance_id
        else:
            # If there's no default setting, you might want to return None or some default value
            return None

    def get_default_instance_for_user(self, user_id):
        default_setting = (
            self.db.query(DBUserDefaultInstance)
            .filter(DBUserDefaultInstance.user_id == user_id)
            .first()
        )
        if default_setting:
            ic("default setting")
            return default_setting
        else:
            ic("no default setting")
            return None

    def get_all_instances_for_user(self, user_id):
        ic("get_all_instances_for_user")
        user = self._get_user_by_username()
        if not user:
            raise ValueError("User not found")
        else:
            all_instances = (
                self.db.query(DBInstance).filter(DBInstance.owner_id == user_id).all()
            )
            all_instances = sorted(all_instances, key=lambda x: x.instance_nickname)
        return all_instances

    def get_instance_by_id_and_username(self, instance_id: int) -> DBInstance:
        ic("get_instance_by_id_and_username")
        user = self._get_user_by_username()
        ic("repository", user)
        if not user:
            raise ValueError("User not found")

        return (
            self.db.query(DBInstance)
            .filter(DBInstance.id == instance_id, DBInstance.owner_id == user.id)
            .first()
        )

    def get_instance_by_id_and_username_pydantic(
        self, instance_id: int
    ) -> SInstanceOut:
        user = self._get_user_by_username()
        if not user:
            raise ValueError("User not found")

        ic(user.id, instance_id)
        instance = (
            self.db.query(DBInstance)
            .filter(DBInstance.id == instance_id, DBInstance.owner_id == user.id)
            .first()
        )

        if instance:
            try:
                instance_password = encryption_manager.decrypt_data(
                    instance.instance_password
                )
            except:
                instance_password = None

            return SInstanceOut(
                id=instance.id,
                url=instance.url,
                instance_user=instance.instance_user,
                instance_nickname=instance.instance_nickname,
                instance_password=instance_password,
                owner_id=instance.owner_id,
                stealth_mode=instance.stealth_mode,  # Add stealth_mode
                xdo_destination=instance.xdo_destination,  # Add xdo_destination
                xdm_destination=instance.xdm_destination,  # Add xdm_destination
            )
        else:
            print(f"Current instance: {instance_id}")
            raise ValueError("Instance not found")

    def get_user_instance_details(self, instance_id: int = None) -> SInstanceOut:
        """
        Fetches instance details for a given instance ID or the user's default instance
        if no ID is provided.

        :param instance_id: Optional. The ID of the instance to fetch. If not provided,
                            the user's default instance will be used.
        :return: An instance of SInstanceOut with the details of the requested or default instance.
        """

        # If an instance ID is provided, use it; otherwise, fetch the default instance ID
        if instance_id is None:
            default_instance_id = self.get_default_instance_id_for_user(
                self._get_user_by_username().id
            )
            if not default_instance_id:
                raise ValueError("No default instance set for user")
            instance_id = default_instance_id

        # Fetch the instance details
        instance_details = self.get_instance_by_id_and_username_pydantic(instance_id)
        if not instance_details:
            raise ValueError("Instance not found")

        return instance_details

    def update_instance(self, instance_id: int, instance_data: SInstanceCreate):
        ic("start update")
        instance = self.get_instance_by_id_and_username(instance_id)
        if instance:
            # Convert the Url object to a string for the database
            url_str = str(instance_data.url)  # Convert Url to string

            if instance.url != url_str:
                instance.url = url_str
            if instance.instance_user != instance_data.instance_user:
                instance.instance_user = instance_data.instance_user
            if instance.instance_nickname != instance_data.instance_nickname:
                instance.instance_nickname = instance_data.instance_nickname

            # Encrypt and update the password if provided and different
            if (
                instance_data.instance_password
                and instance.instance_password != instance_data.instance_password
            ):
                encrypted_password = instance_data.encrypt_instance_password()
                instance.instance_password = encrypted_password

            self.db.commit()
            self.db.refresh(instance)
            ic("finish update")
            return instance

        return None

    def update_instance_details(
        self,
        instance_id: int,
        url: str,
        instance_user: str,
        instance_nickname: str,
        instance_password: str,
    ):
        """
        Update the details of a specific instance.

        :param instance_id: The ID of the instance to update.
        :param url: The new URL for the instance.
        :param instance_user: The new user for the instance.
        :param instance_nickname: The new nickname for the instance.
        """
        # Fetch the instance by ID
        instance = (
            self.db.query(DBInstance).filter(DBInstance.id == instance_id).first()
        )

        if instance:
            # Update the instance details
            instance.url = url
            instance.instance_user = instance_user
            instance.instance_nickname = instance_nickname
            instance.instance_password = instance_password

            # Commit the changes to the database
            try:
                self.db.commit()
                return True  # Indicate success
            except Exception as e:
                # If there's an error during the commit, rollback the transaction
                self.db.rollback()
                print(f"Failed to update instance details: {e}")
                return False  # Indicate failure
        else:
            # If the instance is not found, you might want to handle this case
            print(f"Instance with ID {instance_id} not found.")
            return False  # Indicate the instance was not found

    def update_instance_password(self, instance_id: int, new_encrypted_password: str):
        """
        Update the password for a specific instance.

        :param instance_id: The ID of the instance to update.
        :param new_encrypted_password: The new encrypted password for the instance.
        """
        # Fetch the instance by ID
        instance = (
            self.db.query(DBInstance).filter(DBInstance.id == instance_id).first()
        )

        if instance:
            # Update the instance password with the new encrypted password
            instance.instance_password = new_encrypted_password

            # Commit the changes to the database
            try:
                self.db.commit()
                return True
            except Exception as e:
                # If there's an error during the commit, rollback the transaction
                self.db.rollback()
                print(f"Failed to update instance password: {e}")
                return False
        else:
            # If the instance is not found, you might want to handle this case
            print(f"Instance with ID {instance_id} not found.")
            return False

    def delete_instance(self, instance_id: int):
        # Attempt to fetch the default instance setting for the user that matches the instance_id to be deleted
        default_instance_entry = (
            self.db.query(DBUserDefaultInstance)
            .filter(
                DBUserDefaultInstance.default_instance_id == instance_id,
                DBUserDefaultInstance.user_id
                == self._get_user_by_username().id,  # Assuming this returns the user object
            )
            .first()
        )
        ic(default_instance_entry)
        ic("found default instance entry")

        # If a matching default instance setting is found, delete it
        if default_instance_entry:
            self.db.delete(default_instance_entry)
            self.db.commit()

        # Now, proceed to delete the instance itself
        instance = self.get_instance_by_id_and_username(instance_id)
        if instance:
            try:
                self.db.delete(instance)
                self.db.commit()
                return True  # Indicate successful deletion
            except Exception as e:
                print(f"An error occurred while deleting the instance: {e}")
                self.db.rollback()  # Rollback in case of an error
                return False  # Indicate failure
        else:
            print(
                f"Instance with ID {instance_id} not found or does not belong to user {self.username}."
            )
            return False  # Indicate the instance was not found or doesn't belong to the user

    def get_default_instance_details_view(self):
        """
        Retrieves the details of the default instance for the current user.

        Returns:
            An object containing details of the default instance or None if not found.
        """
        # Fetch the user's default instance details using the view
        default_instance_details = (
            self.db.query(DBUserDefaultInstanceDetail)
            .join(
                DBUser, DBUser.id == DBUserDefaultInstanceDetail.user_id
            )  # Ensure to join with the users table to filter by username
            .filter(DBUser.username == self.username)
            .first()
        )

        if default_instance_details:
            return default_instance_details
        else:
            return None

    def erase_instance_password(self, instance_id: int):
        """
        Erases the password for the specified instance in the database.

        :param instance_id: The ID of the instance for which to erase the password.
        :return: True if the password was successfully erased, False otherwise.
        """
        # Attempt to fetch the instance by its ID
        instance = (
            self.db.query(DBInstance).filter(DBInstance.id == instance_id).first()
        )

        if instance:
            try:
                # Erase the password by setting it to an empty string or None
                instance.instance_password = ""  # or None, depending on your schema
                self.db.commit()
                print(f"Password for instance with ID {instance_id} has been erased.")
                return True
            except Exception as e:
                print(f"An error occurred while erasing the password: {e}")
                self.db.rollback()  # Roll back the transaction in case of an error
                return False
        else:
            print(f"No instance found with ID {instance_id}.")
            return False

    def get_default_instance_details_pydantic(self) -> SUserDefaultInstanceDetail:
        """
        Retrieves the default instance details for the user and returns it as a Pydantic model.

        Returns:
            SUserDefaultInstanceDetail: Pydantic model containing the user's default instance details.
        """
        # Fetch the user's default instance details using the SQLAlchemy model for the view
        default_instance_details = (
            self.db.query(DBUserDefaultInstanceDetail)
            .filter(DBUserDefaultInstanceDetail.username == self.username)
            .first()
        )

        if default_instance_details:
            # Manually instantiate the Pydantic model
            return SUserDefaultInstanceDetail(
                user_id=default_instance_details.user_id,
                username=default_instance_details.username,
                email=default_instance_details.email,
                user_instance_id=default_instance_details.user_instance_id,
                default_instance_url=default_instance_details.default_instance_url,
                default_instance_nickname=default_instance_details.default_instance_nickname,
                instance_password=encryption_manager.decrypt_data(
                    default_instance_details.instance_password
                ),
            )
        else:
            # Return None or raise an exception if the default instance details are not found
            return None

    def get_default_instance_details_pydantic_out(self) -> SInstanceOut:
        """
        Retrieves the default instance details for the user and returns it as a Pydantic model of type SInstanceOut.

        Returns:
            SInstanceOut: Pydantic model containing the details of the user's default instance.
        Raises:
            ValueError: If the user is not found or the user has no default instance set.
        """
        user = self._get_user_by_username()
        if not user:
            raise ValueError("User not found")

        # Fetch the user's default instance ID
        default_instance_id = self.get_default_instance_id_for_user(user.id)
        if not default_instance_id:
            return None
            # raise ValueError("No default instance set for user")

        # Fetch the default instance details
        default_instance = (
            self.db.query(DBInstance)
            .filter(DBInstance.id == default_instance_id)
            .first()
        )
        if not default_instance:
            raise ValueError("Default instance not found")

        # Decrypt the instance password before returning
        print(
            f"WHAT IS MY PASSWORD? {default_instance.instance_password}"
        )  # Already decrypted.

        if default_instance.instance_password:
            decrypted_password = encryption_manager.decrypt_data(
                default_instance.instance_password
            )
        else:
            decrypted_password = None

        return SInstanceOut(
            id=default_instance.id,
            url=default_instance.url,
            instance_user=default_instance.instance_user,
            instance_nickname=default_instance.instance_nickname,
            instance_password=decrypted_password,  # Return the decrypted password
            owner_id=default_instance.owner_id,
            stealth_mode=default_instance.stealth_mode,
            xdo_destination=default_instance.xdo_destination,
            xdm_destination=default_instance.xdm_destination,
        )


class SQLQueriesHistoryRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add_sql_query(
        self,
        user_id: int,
        instance_nickname: str,
        sql_query: str,
        status: str,
        success: bool,
    ):
        new_entry = SQLQueriesHistory(
            user_id=user_id,
            sql_query=sql_query,
            instance_nickname=instance_nickname,
            status=status,
            success=success,
            created_at=datetime.utcnow(),
        )
        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)
        return new_entry

    def get_user_sql_history(self, user_id: int):
        return (
            self.db.query(SQLQueriesHistory)
            .filter(SQLQueriesHistory.user_id == user_id)
            .all()
        )

    def get_user_sql_history_desc(self, user_id: int):
        return (
            self.db.query(SQLQueriesHistory)
            .filter(SQLQueriesHistory.user_id == user_id)
            .order_by(desc(SQLQueriesHistory.created_at))
            .all()
        )

    def get_user_sql_history_desc_days(self, user_id: int, days: int):
        date_threshold = datetime.now() - timedelta(days=days)
        return (
            self.db.query(SQLQueriesHistory)
            .filter(SQLQueriesHistory.user_id == user_id)
            .filter(SQLQueriesHistory.created_at >= date_threshold)
            .order_by(desc(SQLQueriesHistory.created_at))
            .all()
        )


class ChatGPTRequestsHistoryRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add_chatgpt_response(self, user_id: int, chatgpt_response: str):
        new_entry = ChatGPTRequestsHistory(
            user_id=user_id,
            chatgpt_response=chatgpt_response,
            created_at=datetime.utcnow(),
        )
        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)
        return new_entry

    def get_user_chatgpt_history(self, user_id: int):
        return (
            self.db.query(ChatGPTRequestsHistory)
            .filter(ChatGPTRequestsHistory.user_id == user_id)
            .all()
        )


if __name__ == "__main__":

    # Usage example
    def test_user_operations():
        db = SessionLocal()  # Create a new database session
        user_repo = UserRepository(db)

        # Create a user
        new_user = SUserCreate(
            username="testuser", email="test@example.com", password="password123"
        )
        created_user = user_repo.create_user(new_user)
        print(f"Created User: {created_user.username}")

        # Update the user
        updated_user = user_repo.update_user(
            created_user.username, email="newemail@example.com"
        )
        print(f"Updated User Email: {updated_user.email}")

        # Read the user's username
        user = user_repo.get_user_by_username(created_user.username)
        print(f"User's Username: {user.username}")

        # Delete the user
        user_repo.delete_user(created_user.username)
        print("User deleted")

        db.close()

    test_user_operations()
