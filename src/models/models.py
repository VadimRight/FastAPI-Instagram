from sqlalchemy.orm import declarative_base, Mapped, relationship

Base = declarative_base()



import jwt
import bcrypt

from src.config import SECRET
from sqlalchemy import Column, LargeBinary, ForeignKey, Boolean, \
    UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import (
    Integer,
    String,
)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, nullable=False)
    image = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="user")




class User(Base):
    """Models a user table"""
    __tablename__ = "user"
    email = Column(String(225), nullable=False, unique=True)
    id = Column(Integer, nullable=False, primary_key=True)
    hashed_password = Column(LargeBinary, nullable=False)
    username = Column(String(15), nullable=False, )
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    image: Mapped["Image"] = relationship(back_populates="image")

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {username!r}>".format(username=self.username)

    @staticmethod
    def hash_password(password):
        """Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
