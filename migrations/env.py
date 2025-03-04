import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context

# Alembic Config object, providing access to values within the .ini file.
config = context.config

# Ensure that a logging configuration file is provided before configuring logging.
if config.config_file_name:
    fileConfig(config.config_file_name)
else:
    raise ValueError("No logging configuration file provided in the Alembic config.")

logger = logging.getLogger("alembic.env")


def get_engine():
    """
    Retrieve the SQLAlchemy engine from the Flask app.
    Supports both Flask-SQLAlchemy <3 and >=3.
    """
    try:
        # For Flask-SQLAlchemy <3 and Alchemical
        return current_app.extensions["migrate"].db.get_engine()
    except (TypeError, AttributeError):
        # For Flask-SQLAlchemy >=3
        return current_app.extensions["migrate"].db.engine


def get_engine_url():
    """
    Get the engine URL as a string with any percent signs escaped.
    """
    try:
        return get_engine().url.render_as_string(hide_password=False).replace("%", "%%")
    except AttributeError:
        return str(get_engine().url).replace("%", "%%")


# Set the main SQLAlchemy URL in the Alembic config.
config.set_main_option("sqlalchemy.url", get_engine_url())
target_db = current_app.extensions["migrate"].db


def get_metadata():
    """
    Return the metadata object for autogeneration support.
    """
    if hasattr(target_db, "metadatas"):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode. In this mode, only a URL is needed, not an Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode by creating an Engine and associating a connection.
    """

    def process_revision_directives(context, revision, directives):
        """
        Prevent auto-generation of an empty migration script.
        """
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    # Retrieve additional configuration arguments from the Flask-Migrate extension.
    conf_args = current_app.extensions["migrate"].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=get_metadata(), **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine whether to run migrations in offline or online mode.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
