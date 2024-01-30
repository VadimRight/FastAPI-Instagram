from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
import jwt
import bcrypt

from src.config import SECRET, JWT_ALGORITHM
from sqlalchemy import Column, LargeBinary, ForeignKey, Boolean, \
    UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import (
    Integer,
    String,
)


Base = declarative_base()


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class User(Base):
    """Models a user table"""
    __tablename__ = "user"
    email = Column(String(225), nullable=False, unique=True)
    id = Column(Integer, nullable=False, primary_key=True)
    hashed_password = Column(LargeBinary, nullable=False)
    username = Column(String(15), nullable=False, )
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

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

    def validate_password(self, password):
        """Confirms password validity"""
        return {
            "access_token": jwt.encode(
                {"username": self.username, "email": self.email},
                "ApplicationSecretKey"
            )
        }

    def generate_token(self):
        """Generate access token for user"""
        return {
            "access_token": jwt.encode(
                {"username": self.username, "email": self.email},
                SECRET
            )
        }

    def create_access_token(self, exp: int = None) -> bytes:
        to_encode = self.dict()
        if exp is not None:
            to_encode.update({"exp": exp})
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
            to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, SECRET, algorithm=JWT_ALGORITHM
        )
        return encoded_jwt
