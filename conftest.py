import pytest
import psycopg2
from config.config_reader import read_config_data


@pytest.fixture(scope="session")
def psql_connection_dict():
    # Connect to DB
    psql_connection_dict = {}
    databases_string = read_config_data("Postgres", "database")
    databases = databases_string.split(", ")

    for database in databases:
        connection = psycopg2.connect(
            host=read_config_data("Postgres", "host"),
            database=database,
            user=read_config_data("Postgres", "user"),
            password=read_config_data("Postgres", "password"),
            port=read_config_data("Postgres", "port")
        )
        psql_connection_dict[database] = connection
    return psql_connection_dict


@pytest.fixture(scope="session")
def cursor_dict(psql_connection_dict):
    # Create cursor
    cursor_dict = {}
    for key, value in psql_connection_dict.items():
        cursor_dict[key] = value.cursor()
    return cursor_dict


@pytest.fixture(scope="session")
def db_close_connection(psql_connection_dict):
    # Break connection
    yield
    for key, value in psql_connection_dict.items():
        value.close()


@pytest.fixture(scope="session")
def db_close_cursor(cursor_dict):
    # Break cursor
    yield
    for key, value in cursor_dict.items():
        value.close()
