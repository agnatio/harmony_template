import bcrypt
from cryptography.fernet import Fernet

from genpass_folder.crypto_fernet import secret_key


class PasswordManager:
    def generate_bcrypt_hash(self, password):
        # Generate a bcrypt hash for the given password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
        return password_hash.decode("utf-8")

    def verify_password(self, plain_password, hashed_password):
        # Verify if a plain password matches the hashed password
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )


class EncryptionManager:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def encrypt_data(self, data):
        if not isinstance(data, bytes):
            data = data.encode()
        encrypted_data = self.cipher.encrypt(data)
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        if not isinstance(encrypted_data, bytes):
            encrypted_data = encrypted_data.encode()
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode()


if __name__ == "__main__":
    encryption_manager = EncryptionManager(secret_key)

    # Encrypt the data "123"
    data = "another data to crypt"
    encrypted_data = encryption_manager.encrypt_data(data)
    print(f"Encrypted Data: {encrypted_data}")

    # Save the encrypted data to a file crypt.txt
    with open("crypt.txt", "wb") as file:
        file.write(encrypted_data)

    # Read the encrypted data from the file crypt.txt
    with open("crypt.txt", "rb") as file:
        encrypted_data_from_file = file.read()

    # Decrypt the data from the file
    decrypted_data = encryption_manager.decrypt_data(encrypted_data_from_file)

    print(f"Decrypted Data: {decrypted_data}")
