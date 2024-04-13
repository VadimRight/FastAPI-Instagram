from typing import List
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
import bcrypt

from sqlalchemy import UUID, LargeBinary, ForeignKey, Boolean, MetaData, Text
from sqlalchemy import (
    String,
)

metadata = MetaData()
Base = declarative_base(metadata=metadata)


# Model for images
class Post(Base):
    __tablename__ = 'post'
    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(UUID, ForeignKey("user.id"), nullable=False)
    commment: Mapped[List["Comment"]] = relationship() 
    like: Mapped[List["Like_For_Post"]] = relationship()
    

class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("user.id"), nullable=False)
    post_id: Mapped[str] = mapped_column(UUID, ForeignKey("post.id"), nullable=False)
    like: Mapped[List["Like_For_Comment"]] = relationship()


class Like_For_Post(Base):
    __tablename__ = 'likepost'
    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(UUID, ForeignKey("user.id"), nullable=False)
    post_id: Mapped[str] = mapped_column(UUID, ForeignKey("post.id"), nullable=False)


class Like_For_Comment(Base):
    __tablename__ = 'likecomment'
    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("user.id"), nullable=False)
    comment_id: Mapped[str] = mapped_column(UUID, ForeignKey("comment.id"), nullable=False)


#  Model for user
class User(Base):
    """Models a user table"""
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(UUID, nullable=False, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(225), nullable=False, unique=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    username: Mapped[str] = mapped_column(String(15), nullable=False, )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    post: Mapped[List['Post']] = relationship()
    comment: Mapped[List["Comment"]] = relationship()
    likepost: Mapped[List["Like_For_Post"]] = relationship()
    likecomment: Mapped[List["Like_For_Comment"]] = relationship()


 
    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {username!r}>".format(username=self.username)

    @staticmethod
    def hash_password(password):
        """Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
