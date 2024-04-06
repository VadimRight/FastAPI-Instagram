import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
import os, sys
sys.path.append(os.path.join(sys.path[0], 'src'))
from src.config import *
from src.models.models import *
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.


config = context.config

# here we allow ourselves to pass interpolation vars to alembic.ini
# fron the host env
section = config.config_ini_section
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_PASSWORD", DB_PASSWORD)
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_PORT", DB_PORT)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = [Base.metadata]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
