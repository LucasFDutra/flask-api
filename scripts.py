import os
import sys
import json
import importlib
import mugrations
import time


def get_env():
    if ('--prod' in sys.argv):
        os.environ['PROJECT_ENVIRONMENT'] = 'PROD'
    elif ('--test' in sys.argv):
        os.environ['PROJECT_ENVIRONMENT'] = 'TEST'
    else:
        os.environ['PROJECT_ENVIRONMENT'] = 'DEV'


def get_json_config():
    f = open('mugrations_config.json')
    config = json.load(f)
    f.close()
    return config


def end_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def get_connection():
    get_env()
    config = get_json_config()
    connection_path = config['connection_path']

    connection_package = connection_path.replace('.py', '').replace('/', '.')
    connection_function = importlib.import_module(
        connection_package, connection_path)

    connection = connection_function.create_db_connection()
    return connection


def get_mugrations_path():
    config = get_json_config()
    mugrations_path = config['mugrations_path']
    return mugrations_path


def mugrations_init():
    connection = get_connection()
    cursor = connection.cursor()
    mugrations.init(cursor)
    end_connection(connection, cursor)


def mugrations_end():
    connection = get_connection()
    cursor = connection.cursor()
    mugrations.end_mugration(cursor)
    end_connection(connection, cursor)


def mugrations_create_mugration():
    root_path = get_mugrations_path()

    for arg in sys.argv:
        if ('--name=' in arg):
            file_name = arg.replace('--name=', '')
            mugrations.create_mugration(file_name, root_path)


def mugrations_delete_mugration():
    connection = get_connection()
    root_path = get_mugrations_path()
    cursor = connection.cursor()

    for arg in sys.argv:
        if ('--name=' in arg):
            file_name = arg.replace('--name=', '')
            mugrations.delete_mugration(cursor, file_name, root_path)
            end_connection(connection, cursor)


def mugrations_up_all():
    connection = get_connection()
    cursor = connection.cursor()
    root_path = get_mugrations_path()
    package_path = root_path.replace('/', '.')
    mugrations.up_all(cursor, root_path, package_path)
    end_connection(connection, cursor)


def mugrations_down_all():
    connection = get_connection()
    cursor = connection.cursor()
    root_path = get_mugrations_path()
    package_path = root_path.replace('/', '.')
    mugrations.down_all(cursor, root_path, package_path)
    end_connection(connection, cursor)


def mugrations_down_latest():
    connection = get_connection()
    cursor = connection.cursor()
    root_path = get_mugrations_path()
    package_path = root_path.replace('/', '.')
    mugrations.down_latest(cursor, root_path, package_path)
    end_connection(connection, cursor)


def mugrations_help():
    mugrations.help_function()


def test():
    sys.argv.append('--test')
    os.system("docker start postgres-test")
    time.sleep(3)
    mugrations_init()
    mugrations_up_all()
    os.system("pytest --cov=./flask-api/src --cov-report=xml")
    time.sleep(3)
    mugrations_down_all()
    mugrations_end()
    os.system("docker stop postgres-test")
