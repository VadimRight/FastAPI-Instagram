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
import pprint

engine = create_engine("sqlite://")

with engine.begin() as conn:
    conn.execute(
        text(
            '''
                create table foo (
                    id integer not null primary key,
                    old_data varchar,
                    x integer
                )
            '''
        )
    )
    conn.execute(text("create table bar (data varchar)"))


Table(
    "image",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("image", String, nullable=False)
)


mc = MigrationContext.configure(engine.connect())

diff = compare_metadata(mc, metadata)
pprint.pprint(diff, indent=2, width=20)