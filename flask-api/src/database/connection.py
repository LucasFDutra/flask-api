import psycopg2
from dotenv import load_dotenv
import os


def create_db_connection():
    load_dotenv()
    environment = os.environ['PROJECT_ENVIRONMENT']
    if (environment == 'PROD'):
        connection_params = {
            'dbname': os.environ['FLASK_API_DBNAME_PROD'],
            'user': os.environ['FLASK_API_USER_PROD'],
            'password': os.environ['FLASK_API_PASSWORD_PROD'],
            'host': os.environ['FLASK_API_HOST_PROD'],
            'port': os.environ['FLASK_API_PORT_PROD']
        }

    elif (environment == 'DEV'):
        connection_params = {
            'dbname': os.environ['FLASK_API_DBNAME_DEV'],
            'user': os.environ['FLASK_API_USER_DEV'],
            'password': os.environ['FLASK_API_PASSWORD_DEV'],
            'host': os.environ['FLASK_API_HOST_DEV'],
            'port': os.environ['FLASK_API_PORT_DEV']
        }

    elif (environment == 'TEST'):
        connection_params = {
            'dbname': os.environ['FLASK_API_DBNAME_TEST'],
            'user': os.environ['FLASK_API_USER_TEST'],
            'password': os.environ['FLASK_API_PASSWORD_TEST'],
            'host': os.environ['FLASK_API_HOST_TEST'],
            'port': os.environ['FLASK_API_PORT_TEST']
        }

    connection = psycopg2.connect(**connection_params)

    return connection
