from time import time
from src.database import connection
import importlib
import os
import sys


def init(cursor):
    cursor.execute("""
        CREATE TABLE mugrations (
            id_mugration_pk SERIAL PRIMARY KEY,
            mugration_file TEXT NOT NULL,
            mugration_file_status BOOLEAN NOT NULL
        )
    """)


def get_mugrations_list(cursor):
    cursor.execute("SELECT * FROM mugrations ORDER BY id_mugration_pk")
    response = cursor.fetchall()
    return response


def set_mugration_in_db(cursor, file_name):
    cursor.execute("""
        INSERT INTO mugrations (
            mugration_file, mugration_file_status
        ) VALUES (%s, %s)
    """, (file_name, False))


def update_mugration_value(cursor, id_mugration, status):
    cursor.execute("""
        UPDATE mugrations SET mugration_file_status = {} WHERE id_mugration_pk = {}
    """.format(status, id_mugration))


def create_mugration(cursors, file_name, root_path):
    mugration_file_name = 'mugration_'+str(time()).replace(
        '.', '_')+'_'+file_name.replace('--name=', '')
    mugration_file_name_ex = root_path+mugration_file_name+'.py'
    os.system('touch '+mugration_file_name_ex)
    for cursor in cursors:
        set_mugration_in_db(cursor, mugration_file_name)


def delete_mugration(cursors, file_name, root_path):
    mugration_file_name = file_name.replace('--name=', '')
    mugration_file_name_ex = mugration_file_name+'.py'

    for cursor in cursors:
        cursor.execute("""
            SELECT * FROM mugrations WHERE mugration_file = '{}'
        """.format(mugration_file_name))
        response = cursor.fetchall()

        if (len(response) == 0):
            print("file does't exist in database")
            return False

        id_mugration = response[0][0]
        cursor.execute("""
            DELETE FROM mugrations WHERE id_mugration_pk = {}
        """.format(id_mugration))

    os.system('rm '+root_path+mugration_file_name_ex)


def validate_files(files_list_in_db, root_path):
    files_list = os.listdir(root_path)
    files_names = []

    # coletando apenas os arquivos de migrations
    for file_name in files_list:
        if ('mugration_' in file_name):
            files_names.append(file_name)

    if (len(files_names) > 0):
        files_list = files_names
    else:
        print("you don't have mugrations files")
        return False

    # verificar se existe registro no db
    if (len(files_list_in_db) == 0):
        print('database is empty')
        return False

    files_in_db = [row[1]+'.py' for row in files_list_in_db]

    # ver duplicata de arquivos
    for file_name in files_list:
        if (files_list.count(file_name) > 1):
            print('there are two files with the same name')
            return False

    # confirmar se todos os arquivos estão registrados no banco
    for file_name in files_list:
        if not (file_name in files_in_db):
            print("the file doesn't exist in the database ", file_name)
            return False

    # verificar se os registros que tem no banco estão dentre os arquivos
    for file_in_db in files_in_db:
        if not (file_in_db in files_list):
            print("update your mugrations files, you don't have ", file_in_db)
            return False

    return True


def down_latest(cursor, root_path, package_path):
    files_list_in_db = get_mugrations_list(cursor)
    response = validate_files(files_list_in_db, root_path)
    if (response):
        for i in range(len(files_list_in_db)-1, -1, -1):
            row = files_list_in_db[i]
            if (row[2]):
                id_mugration = row[0]
                mugration_file_name = row[1]
                mugration_file_name_ex = mugration_file_name+'.py'
                module_name = package_path+mugration_file_name
                module_path = root_path+mugration_file_name_ex
                down_function = importlib.import_module(
                    module_name, module_path)
                down_function.down(cursor)
                update_mugration_value(cursor, id_mugration, False)
                break


def up_all(cursor, root_path, package_path):
    files_list_in_db = get_mugrations_list(cursor)
    response = validate_files(files_list_in_db, root_path)
    if (response):
        for row in files_list_in_db:
            id_mugration = row[0]
            mugration_file_name = row[1]
            mugration_file_name_ex = mugration_file_name+'.py'
            module_name = package_path+mugration_file_name
            module_path = root_path+mugration_file_name_ex
            up_function = importlib.import_module(module_name, module_path)
            if (not row[2]):
                up_function.up(cursor)
                update_mugration_value(cursor, id_mugration, True)


def down_all(cursor, root_path, package_path):
    files_list_in_db = get_mugrations_list(cursor)
    response = validate_files(files_list_in_db, root_path)
    if (response):
        for row in files_list_in_db:
            if (row[2]):
                id_mugration = row[0]
                mugration_file_name = row[1]
                mugration_file_name_ex = mugration_file_name+'.py'
                module_name = package_path+mugration_file_name
                module_path = root_path+mugration_file_name_ex
                down_function = importlib.import_module(
                    module_name, module_path)
                down_function.down(cursor)
                update_mugration_value(cursor, id_mugration, False)


def help_function():
    print('--init                create mugrations table')
    print('--down_latest         rollback the most recent action record in the mugrations table')
    print('--up_all              run all mugration files that have not yet been run')
    print('--down_all            rollback all actions register in mugrations table')
    print('--create_mugration    create a mugration file with a name, specify the name using --name=mugration_name')
    print('--delete_mugration    delete the mugration file and remove its record from the database, you must pass the full file name (without .py) in the flag --name=file_name')


if __name__ == "__main__":
    current_path_to_mugration_path = '/src/database/mugrations/'
    package_path = current_path_to_mugration_path.replace('/', '.')[1:]
    args = sys.argv
    this_file_path = os.path.abspath(__file__)
    root_path = '/'.join(this_file_path.split('/')
                         [:-1])+current_path_to_mugration_path

    if ('--prod' in args):
        os.environ['PROJECT_ENVIRONMENT'] = 'PROD'
    elif ('--test' in args):
        os.environ['PROJECT_ENVIRONMENT'] = 'TEST'
    else:
        os.environ['PROJECT_ENVIRONMENT'] = 'DEV'

    connection_mg = connection.create_db_connection()
    cursor = connection_mg.cursor()

    if ('--init' in args):
        for env in ['PROD', 'TEST', 'DEV']:
            os.environ['PROJECT_ENVIRONMENT'] = env
            connection_mg = connection.create_db_connection()
            cursor = connection_mg.cursor()
            init(cursor)
            connection_mg.commit()
            cursor.close()

    elif ('--down_latest' in args):
        down_latest(cursor, root_path, package_path)

    elif ('--up_all' in args):
        up_all(cursor, root_path, package_path)

    elif ('--down_all' in args):
        down_all(cursor, root_path, package_path)

    elif ('--create_mugration' in args):
        file_name = args[2]
        if ('--name=' in file_name):
            cursors = []
            connections = []
            for env in ['PROD', 'TEST', 'DEV']:
                os.environ['PROJECT_ENVIRONMENT'] = env
                connection_mg = connection.create_db_connection()
                cursor = connection_mg.cursor()
                connections.append(connection_mg)
                cursors.append(cursor)
            create_mugration(cursors, file_name, root_path)
            for i in range(len(connections)):
                connections[i].commit()
                cursors[i].close()
        else:
            print('name is missing')

    elif ('--delete_mugration' in args):
        file_name = args[2]
        if ('--name=' in file_name):
            cursors = []
            connections = []
            for env in ['PROD', 'TEST', 'DEV']:
                os.environ['PROJECT_ENVIRONMENT'] = env
                connection_mg = connection.create_db_connection()
                cursor = connection_mg.cursor()
                connections.append(connection_mg)
                cursors.append(cursor)
            delete_mugration(cursors, file_name, root_path)
            for i in range(len(connections)):
                connections[i].commit()
                cursors[i].close()
        else:
            print('name is missing')

    elif ('--help' in args):
        help_function()

    else:
        print("This action don't exist")

    connection_mg.commit()
    cursor.close()
