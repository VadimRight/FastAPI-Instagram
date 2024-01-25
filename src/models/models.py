from sqlalchemy_imageattach.entity import image_attachment

from src.database import Base, metadata

from sqlalchemy import Column, Integer, Text, MetaData, String, create_engine, LargeBinary, ForeignKey
from sqlalchemy import (
    Integer,
    String,
    Table,
    text,
)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String(length=24), nullable=False)
    email = Column(String, nullable=False, unique=True)
    __tablename__ = 'user'


