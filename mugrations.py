from time import time
import importlib
import os


def get_mugrations_list(cursor):
    cursor.execute("SELECT * FROM mugrations ORDER BY id_mugration_pk")
    response = cursor.fetchall()
    return response


def set_mugration_in_db(cursor, file_name):
    cursor.execute("""
        INSERT INTO mugrations (
            mugration_file, mugration_file_status
        ) VALUES (%s, %s)
    """, (file_name, True))


def update_mugration_value(cursor, id_mugration, status):
    cursor.execute("""
        UPDATE mugrations SET mugration_file_status = {} WHERE id_mugration_pk = {}
    """.format(status, id_mugration))


def get_mugration_files(root_path):
    files_names = []
    files_list = os.listdir(root_path)
    for file_name in files_list:
        if ('mugration_' in file_name):
            files_names.append(file_name)
    files_names.sort()
    return files_names


def validate_files(files_list_in_db, files_list, root_path, action):
    files_names_in_db = [row[1]+'.py' for row in files_list_in_db]

    if (len(files_list) == 0):
        print("you don't have mugrations files")
        return False

    # verificações exclusivas para os métodos down
    if (action == 'down'):
        # verificar se existe registro no db no momento de down
        if (len(files_list_in_db) == 0):
            print('database is empty')
            return False

        # confirmar se todos os arquivos estão registrados no banco
        for file_name in files_list:
            if not (file_name in files_names_in_db):
                print("the file doesn't exist in the database ", file_name)
                return False

    # ver duplicata de arquivos
    for file_name in files_list:
        if (files_list.count(file_name) > 1):
            print('there are two files with the same name')
            return False

    # verificar se os registros que tem no banco estão dentre os arquivos
    for file_in_db in files_names_in_db:
        if not (file_in_db in files_list):
            print("update your mugrations files, you don't have ", file_in_db)
            return False

    return True


def init(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mugrations (
            id_mugration_pk SERIAL PRIMARY KEY,
            mugration_file TEXT NOT NULL,
            mugration_file_status BOOLEAN NOT NULL
        )
    """)


def end_mugration(cursor):
    cursor.execute("""
        DROP TABLE mugrations
    """)


def create_mugration(file_name, root_path):
    mugration_file_name = 'mugration_'+str(time()).replace(
        '.', '_')+'_'+file_name.replace('--name=', '')
    mugration_file_name_ex = root_path+mugration_file_name+'.py'
    os.system('touch '+mugration_file_name_ex)


def delete_mugration(cursor, file_name, root_path):
    mugration_file_name = file_name.replace('--name=', '')
    mugration_file_name_ex = mugration_file_name+'.py'

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


def up_all(cursor, root_path, package_path):
    files_list_in_db = get_mugrations_list(cursor)
    files_list = get_mugration_files(root_path)
    response = validate_files(files_list_in_db, files_list, root_path, 'up')

    files_list_in_db_array = [row[1] for row in files_list_in_db]

    if (response):
        for file_name in files_list:
            mugration_file_name = file_name.replace('.py', '')
            mugration_file_name_ex = file_name
            module_name = package_path+mugration_file_name
            module_path = root_path+mugration_file_name_ex
            up_function = importlib.import_module(module_name, module_path)
            if (len(files_list_in_db_array) > 0 and mugration_file_name in files_list_in_db_array):
                location = files_list_in_db_array.index(mugration_file_name)
                [id_mugration, file_name_in_db, status] = files_list_in_db[location]
                if (not status):
                    up_function.up(cursor)
                    update_mugration_value(cursor, id_mugration, True)
            else:
                up_function.up(cursor)
                set_mugration_in_db(cursor, mugration_file_name)


def down_all(cursor, root_path, package_path):
    files_list_in_db = get_mugrations_list(cursor)
    files_list = get_mugration_files(root_path)

    response = validate_files(files_list_in_db, files_list, root_path, 'down')

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


def down_latest(cursor, root_path, package_path):
    files_list_in_db = get_mugrations_list(cursor)
    files_list = get_mugration_files(root_path)

    response = validate_files(files_list_in_db, files_list, root_path, 'down')

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


def help_function():
    print('--init                create mugrations table')
    print('--end_mugration       drop mugrations table')
    print('--down_latest         rollback the most recent action record in the mugrations table')
    print('--up_all              run all mugration files that have not yet been run')
    print('--down_all            rollback all actions register in mugrations table')
    print('--create_mugration    create a mugration file with a name, specify the name using --name=mugration_name')
    print('--delete_mugration    delete the mugration file and remove its record from the database, you must pass the full file name (without .py) in the flag --name=file_name')
