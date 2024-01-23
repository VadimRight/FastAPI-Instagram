from alembic.autogenerate import compare_metadata
from alembic.runtime.migration import MigrationContext
from pydantic import Json
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.database import Base, metadata

from sqlalchemy import Column, Integer, Text, MetaData, String, create_engine
from sqlalchemy import (
    Integer,
    String,
    Table,
    text,
)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, index=True)


