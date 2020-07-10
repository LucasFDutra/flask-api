import os
import sys
import pandas as pd


def up():
    for file_name in list_files:
        if not (file_name in forbidden_files):
            print('file: ', file_name)
            os.system('python3 '+root_path+'/' + str(file_name)+' --up')


def down():
    for file_name in list_files:
        if not (file_name in forbidden_files):
            print('file: ', file_name)
            os.system('python3 '+root_path+'/' + str(file_name)+' --down')


if __name__ == "__main__":
    this_file_path = os.path.abspath(__file__)
    root_path = '/'.join(this_file_path.split('/')[:-1])+'/migrations'
    list_files = os.listdir(root_path)
    forbidden_files = ['__pycache__', '__init__.py',
                       'migrationsConnection.py', 'migrations_list.csv']

    if ('--up' in sys.argv):
        up()
    elif ('--down' in sys.argv):
        down()
