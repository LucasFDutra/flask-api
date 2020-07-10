from time import time
import os
import sys

print(sys.argv)

arg_name = sys.argv[1]

migration_file_name = str(time()).replace(
    '.', '_')+'_'+arg_name.replace('--name=', '')
this_file_path = os.path.abspath(__file__).split('/')[:-1]
this_file_path.append(this_file_path[-1])
migration_file_path = '/'.join(this_file_path)+'/src/database/migrations/'
migration_file_name = migration_file_path+migration_file_name+'.py'
print(migration_file_name)
os.system('touch '+migration_file_name)
