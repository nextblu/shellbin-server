# using mysqlclient requires the mysql-connector-c C library to work.
import MySQLdb

from config import DatabaseConfig
from tentalog import Tentacle


logger = Tentacle().logger

# @todo: Integrate the context manager and the pool of connections

class Database:
    def __init__(self):
        self.__host = DatabaseConfig.HOST
        self.__user = DatabaseConfig.USER
        self.__password = DatabaseConfig.PASSWORD
        self.__database = DatabaseConfig.DB_NAME
        self.__charset = 'ascii'
        self.__connection = MySQLdb.connect(
            self.__host, self.__user, self.__password, self.__database, charset=self.__charset
        )
        self.__cursor = None
        logger.debug(f"Database initialized at {self.__host} with name {self.__database}")

    def get_cursor(self):
        # Always forcing to use prepared statements
        # If there was a previous
        if self.__cursor:
            self.__cursor.close()
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def done(self):
        try:
            self.__connection.commit()
        except MySQLdb.Error as e:
            self.__connection.rollback()
            return DatabaseError(repr(e))

    def __del__(self):
        self.__connection.close()


class DatabaseError(Exception):
    def __init__(self, message):
        super().__init__(message)
