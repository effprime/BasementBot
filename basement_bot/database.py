"""Provides an interface for database sessions.
"""

import api
import logger
import sqlalchemy

log = logger.get_logger("Database")


class DatabaseAPI(api.BotAPI):
    """API for accessing a database.

    parameters:
        bot (BasementBot): the bot object
        echo (bool): True for verbose logging
    """

    def __init__(self, bot, echo=False):
        super().__init__(bot)
        self.db_string = self._get_db_string()
        log.debug(f"Connecting to DB: {self.db_string}")
        self.engine = sqlalchemy.create_engine(self.db_string, echo=echo)

    def get_session(self):
        """Creates a session instance."""
        return sqlalchemy.orm.sessionmaker(bind=self.engine)()

    def create_table(self, table):
        """Wraps table creation.

        parameters:
            table (self.Table): the table class
        """
        try:
            log.debug(f"Attempting to create table {table.__name__}")
            table.__table__.create(self.engine, checkfirst=True)
        except sqlalchemy.exc.InvalidRequestError:
            log.debug(f"Table {table.__name__} already exists - ignoring")

    def _get_db_string(self):
        """Gathers database environmental information."""
        user = self.bot.config.main.database.user
        password = self.bot.config.main.database.password
        name = self.bot.config.main.database.name
        host = self.bot.config.main.database.host
        port = self.bot.config.main.database.port
        prefix = self.bot.config.main.database.prefix
        return f"{prefix}://{user}:{password}@{host}:{port}/{name}"
