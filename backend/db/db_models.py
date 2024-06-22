from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    Float,
    JSON,  # Add JSON import for databases that support it
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.db_init import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=False, index=True)
    hashed_password = Column(String)
    is_superuser = Column(Boolean, default=False)
    last_login_time = Column(DateTime)
    last_logout_time = Column(DateTime)
    instances = relationship("Instance", back_populates="owner")
    sql_queries_history = relationship("SQLQueriesHistory", back_populates="user")
    chatgpt_requests_history = relationship(
        "ChatGPTRequestsHistory", back_populates="user"
    )
    default_instance = relationship(
        "UserDefaultInstance", back_populates="user", uselist=False
    )
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())


class Instance(Base):
    __tablename__ = "instances"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    instance_nickname = Column(String)
    instance_user = Column(String, index=True)
    instance_password = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="instances")
    stealth_mode = Column(Boolean, default=False)
    xdo_destination = Column(String)
    xdm_destination = Column(String)
    notes = Column(String)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())


class UserDefaultInstance(Base):
    __tablename__ = "user_default_instances"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    default_instance_id = Column(Integer, ForeignKey("instances.id"))
    user = relationship("User", back_populates="default_instance")
    default_instance = relationship("Instance")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())


class UserDefaultInstanceDetail(Base):
    __tablename__ = (
        "user_default_instance_details"  # The name of the view in the database
    )
    user_id = Column(
        Integer, primary_key=True
    )  # 'user_id' as a primary key for the view
    username = Column(String)
    email = Column(String)
    user_instance_id = Column(
        Integer
    )  # Corresponds to the 'instances.id' column in the view
    default_instance_url = Column(String)
    default_instance_nickname = Column(String)
    instance_password = Column(
        String
    )  # Added to represent the 'instance_password' column


class SQLQueriesHistory(Base):
    __tablename__ = "sql_queries_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sql_queries_history")
    instance_nickname = Column(Text)
    sql_query = Column(Text)
    status = Column(Text)
    success = Column(Boolean)
    is_max = Column(Boolean)
    plsql_regime = Column(Boolean)
    result = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class ChatGPTRequestsHistory(Base):
    __tablename__ = "chatgpt_requests_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="chatgpt_requests_history")
    chatgpt_response = Column(Text)
    request_sent = Column(Text)
    tokens = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Dummy(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())
