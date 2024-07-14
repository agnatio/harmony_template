from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import MetaData
from alembic import context
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# This import should be adjusted based on your project structure
from app.db.db_models import Base, metadata

# Set up logging configuration
config = context.config
fileConfig(config.config_file_name)

# Define the target metadata
target_metadata = Base.metadata


# Ensure the database URL is set correctly
def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
