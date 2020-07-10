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


def up_latest(cursor, root_path, package_path):
    files_list = os.listdir(root_path)
    for file_name in files_list:
        if ('mugration_' in file_name):
            file_name_ = file_name.replace('.py', '')
            module_name = package_path+file_name_
            module_path = root_path+file_name
            up_function = importlib.import_module(module_name, module_path)
            up_function.up(cursor)
            break


def down_latest(cursor, root_path, package_path):
    files_list = os.listdir(root_path)
    for file_name in files_list:
        if ('mugration_' in file_name):
            file_name_ = file_name.replace('.py', '')
            module_name = package_path+file_name_
            module_path = root_path+file_name
            up_function = importlib.import_module(module_name, module_path)
            up_function.down(cursor)
            break


def up_all(cursor, root_path, package_path):
    files_list = os.listdir(root_path)
    for file_name in files_list:
        if ('mugration_' in file_name):
            file_name_ = file_name.replace('.py', '')
            module_name = package_path+file_name_
            module_path = root_path+file_name
            up_function = importlib.import_module(module_name, module_path)
            up_function.up(cursor)


def down_all(cursor, root_path, package_path):
    files_list = os.listdir(root_path)
    for file_name in files_list:
        if ('mugration_' in file_name):
            file_name_ = file_name.replace('.py', '')
            module_name = package_path+file_name_
            module_path = root_path+file_name
            up_function = importlib.import_module(module_name, module_path)
            up_function.down(cursor)


def create_mugration(file_name, root_path):
    mugration_file_name = 'mugration_'+str(time()).replace(
        '.', '_')+'_'+file_name.replace('--name=', '')

    mugration_file_name = root_path+mugration_file_name+'.py'

    print(mugration_file_name)
    os.system('touch '+mugration_file_name)


def down():
    for file_name in list_files:
        if not (file_name in forbidden_files):
            print('file: ', file_name)
            os.system('python3 '+root_path+'/' + str(file_name)+' --down')


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

    elif ('--up_latest' in args):
        up_latest(cursor, root_path, package_path)

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

    connection.commit()
    cursor.close()
    connection.close()

    # list_files = os.listdir(root_path)
    # forbidden_files = ['__pycache__', '__init__.py',
    #                    'mugrationsConnection.py', 'mugrations_list.csv']

#     if ('--up' in sys.argv):
#         up()
#     elif ('--down' in sys.argv):
#         down()


# print(sys.argv)

# arg_name = sys.argv[1]

# mugration_file_name = str(time()).replace(
#     '.', '_')+'_'+arg_name.replace('--name=', '')
# this_file_path = os.path.abspath(__file__).split('/')[:-1]
# this_file_path.append(this_file_path[-1])
# mugration_file_path = '/'.join(this_file_path)+'/src/database/mugrations/'
# mugration_file_name = mugration_file_path+mugration_file_name+'.py'
# print(mugration_file_name)
# os.system('touch '+mugration_file_name)
