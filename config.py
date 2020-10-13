import os


class DatabaseConfig:
    HOST = os.getenv("SHELLBIN_DATABASE_HOST", "localhost")
    USER = os.getenv("SHELLBIN_DATABASE_USER", "root")
    PASSWORD = os.getenv("SHELLBIN_DATABASE_PASSWORD", "root")
    DB_NAME = os.getenv("SHELLBIN_DATABASE_NAME", "shellbin")


class TimeConfig:
    DEFAULT = "Europe/Rome"


class DataSize:
    AUTH_TOKEN_SIZE = 127
    UNSIGNED_INT_MAX = 4294967295
