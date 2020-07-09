import psycopg2
from dotenv import load_dotenv
import os


def create_db_connection():
    load_dotenv()
    connection_params = {
        'dbname': os.environ['FLASK-API_DBNAME'],
        'user': os.environ['FLASK-API_USER'],
        'password': os.environ['FLASK-API_PASSWORD'],
        'host': os.environ['FLASK-API_HOST'],
        'port': os.environ['FLASK-API_PORT']
    }

    connection = psycopg2.connect(**connection_params)

    return connection
