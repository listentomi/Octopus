import pandas as pd
import re
import sqlite3
import os
import numpy as np
import pandas as pd
import re
import sqlite3
import os
import numpy as np
import sys

def process_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".db"):
            file_path = os.path.join(folder_path, file_name)
            process_file(file_path)

def process_file(file_path):
    base_name = os.path.basename(file_path)
    database, file_extension = os.path.splitext(base_name)  # 分离文件名和后缀
    print(file_path)
    # connect to the database
    mydb = connect_db(file_path)
    

    # get all table names
    cursor = mydb.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [i[0] for i in cursor.fetchall()]
    cursor.close()

    # get table info and foreign keys for all tables
    df1 = pd.concat([get_table_info(mydb, table) for table in tables], ignore_index=True)
    df2 = pd.concat([get_foreign_keys(mydb, table) for table in tables], ignore_index=True)

    # replace column types
    replacements = {
        'varchar': 'text',
        'char': 'text',
        'enum': 'categorical',
        'decimal': 'number',
        'float': 'number',
        'double': 'number',
        'date': 'time',
        'year': 'time',
        'datetime': 'time',
        'month':'time',
        'int': 'text',
        'integer': 'text',
        'text': 'text',
        'time': 'time',
        'real': 'number'
    }

    def replace_with_dict(val, dict_):
        val = val.lower()
        for k, v in dict_.items():
            if k in val:
                return v
        return val

    df1['column_types'] = df1['column_types'].apply(lambda x: replace_with_dict(x, replacements))
    df1 = df1.sort_values('table_names')
    df1['column_names'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df1 = df1[df1['column_names'].notna()]

    df = pd.concat([df1, df2], axis=1)
    pattern = '[^\w]'
    database = re.sub(pattern, '_', database)
    output_folder = os.path.join(os.getcwd(), 'info')
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f'{database}.xlsx')
    df.to_excel(output_path, index=False)

def connect_db(data_path):
    conn = sqlite3.connect(data_path)
    return conn

def get_table_info(mydb, table_name):
    try:
        cursor = mydb.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        rows = cursor.fetchall()
        col_names = [i[1] for i in rows]  # column names
        col_types = [i[2] for i in rows]  # column types
        cursor.close()
        return pd.DataFrame({
            'table_names': table_name,
            'table_names_original': table_name,
            'column_names': col_names,
            'column_names_original': col_names,
            'column_types': col_types,
            'column_comment': ['' for _ in col_names],  # SQLite does not support column comments
            'primary_key_name': ['' for _ in col_names]  # SQLite does not support named primary keys
        })
    except Exception as e:
        return None

def get_foreign_keys(mydb, table_name):
    cursor = mydb.cursor()
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    rows = cursor.fetchall()
    cursor.close()
    return pd.DataFrame({
        'origin_table': table_name,
        'origin_column': [i[3] for i in rows],  # from column
        'referenced_table_name': [i[2] for i in rows],  # table
        'referenced_column_name': [i[4] for i in rows]  # to column
    })

# specify the folder path
folder_path = sys.argv[1]
# process files in the folder
process_files_in_folder(folder_path)
# process_file(folder_path)
