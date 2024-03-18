from typing import List
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column

Base = declarative_base()



import jwt
import bcrypt

from src.config import SECRET
from sqlalchemy import Column, LargeBinary, ForeignKey, Boolean, Text, \
    UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import (
    Integer,
    String,
)

# Model for images
class Post(Base):

    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship()


class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)   
    user: Mapped["User"] = relationship()
    post: Mapped["Post"] = relationship() 


class Like(Base):
    __tablename__ = 'like'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, ForeignKey("comment.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"))
    user: Mapped["User"] = relationship()
    post: Mapped["Post"] = relationship() 
    comment: Mapped["Comment"] = relationship()


#  Model for user
class User(Base):
    """Models a user table"""
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(225), nullable=False, unique=True)
    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True, index=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    username: Mapped[str] = mapped_column(String(15), nullable=False, )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    image: Mapped[List['Post']] = relationship()

 
    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {username!r}>".format(username=self.username)

    @staticmethod
    def hash_password(password):
        """Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
