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
    cursor.execute("SELECT * FROM mugrations")
    response = cursor.fetchall()
    return response


def set_migration_in_db(cursor, file_name):
    cursor.execute("""
        INSERT INTO mugrations (
            mugration_file, mugration_file_status
        ) VALUES (%s, %s)
    """, (file_name, True))


def update_migration_value(cursor, file_name, status):
    cursor.execute("""
        UPDATE mugrations SET mugration_file_status = %s WHERE mugration_file = %s
    """, (status, file_name))


def create_mugration(file_name, root_path):
    mugration_file_name = 'mugration_'+str(time()).replace(
        '.', '_')+'_'+file_name.replace('--name=', '')
    mugration_file_name = root_path+mugration_file_name+'.py'
    os.system('touch '+mugration_file_name)


def down_latest(cursor, root_path, package_path):
    files_list_in_db = get_mugrations_list(cursor)
    row = files_list_in_db[-1]
    file_name = row[1]
    file_name_ = file_name.replace('.py', '')
    module_name = package_path+file_name_
    module_path = root_path+file_name
    up_function = importlib.import_module(module_name, module_path)
    up_function.down(cursor)
    update_migration_value(cursor, file_name, False)


def up_all(cursor, root_path, package_path):
    files_list = os.listdir(root_path)
    files_list.sort()
    files_list_in_db = get_mugrations_list(cursor)

    for row in files_list_in_db:
        if not (row[1] in files_list):
            print("update your mugrations files, you don't have ", row[1])
            return 0

    for file_name in files_list:
        if ('mugration_' in file_name):
            file_name_ = file_name.replace('.py', '')
            module_name = package_path+file_name_
            module_path = root_path+file_name
            up_function = importlib.import_module(module_name, module_path)
            identifier = True
            for row in files_list_in_db:
                if (file_name == row[1] and not row[2]):
                    up_function.up(cursor)
                    update_migration_value(cursor, file_name, True)
                    identifier = False
                    break
                elif (file_name == row[1] and row[2]):
                    identifier = False

            if (identifier):
                up_function.up(cursor)
                set_migration_in_db(cursor, file_name)


def down_all(cursor, root_path, package_path):
    files_list = os.listdir(root_path)
    files_list_in_db = get_mugrations_list(cursor)

    for row in files_list_in_db:
        if not (row[1] in files_list):
            print("update your mugrations files, you don't have ", row[1])
            return 0

    for row in files_list_in_db:
        file_name = row[1]
        file_name_ = file_name.replace('.py', '')
        module_name = package_path+file_name_
        module_path = root_path+file_name
        up_function = importlib.import_module(module_name, module_path)
        up_function.down(cursor)
        update_migration_value(cursor, file_name, False)


def help_function():
    print('--init                create mugrations table')
    print('--down_latest         rollback the most recent action record in the mugrations table')
    print('--up_all              run all migration files that have not yet been run')
    print('--down_all            rollback all actions register in mugrations table')
    print('--create_mugration    create a mugration file with a name, specify the name using --name=mugration_name')


if __name__ == "__main__":
    connection = connection.create_db_connection()
    cursor = connection.cursor()
    current_path_to_mugration_path = '/src/database/mugrations/'
    package_path = current_path_to_mugration_path.replace('/', '.')[1:]
    args = sys.argv
    this_file_path = os.path.abspath(__file__)
    root_path = '/'.join(this_file_path.split('/')
                         [:-1])+current_path_to_mugration_path

    if ('--init' in args):
        init(cursor)

    elif ('--down_latest' in args):
        down_latest(cursor, root_path, package_path)

    elif ('--up_all' in args):
        up_all(cursor, root_path, package_path)

    elif ('--down_all' in args):
        down_all(cursor, root_path, package_path)

    elif ('--create_mugration' in args):
        file_name = args[2]
        if ('--name=' in file_name):
            create_mugration(file_name, root_path)
        else:
            print('name is missing')
    elif ('--help' in args):
        help_function()
    else:
        print("This action don't exist")

    connection.commit()
    cursor.close()
    connection.close()
