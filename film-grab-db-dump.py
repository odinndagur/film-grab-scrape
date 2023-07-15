import os
current_db_path = 'film-grab-db0.sqlite3'
os.system(f'sqlite3 {current_db_path} ".dump" > {current_db_path}.txt')

with open(f'{current_db_path}.txt', 'r') as f:
    