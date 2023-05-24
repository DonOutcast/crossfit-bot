from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer,
    Float,
    String,
    Column,
    DateTime,
    LargeBinary,
    ForeignKeyConstraint
)

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    user_name = Column(String(50), nullable=False)
    account_id = Column(Integer(), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(10), nullable=False)
    image = Column(LargeBinary(), nullable=True)
    height = Column(Float(), nullable=True)
    weight = Column(Float(), nullable=True)


