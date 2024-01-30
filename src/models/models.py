from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy_imageattach.entity import image_attachment


from sqlalchemy import Column, Integer, Text, MetaData, String, create_engine, LargeBinary, ForeignKey, Boolean
from sqlalchemy import (
    Integer,
    String,
    Table,
    text,
)

Base = declarative_base()


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)


# class User(Base):
#     id = Column(Integer, primary_key=True)
#     username = Column(String, nullable=False, unique=True)
#     hashed_password: str = Column(String(length=24), nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     __tablename__ = 'user'


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    username: Mapped[str] = mapped_column(String(length=20), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
