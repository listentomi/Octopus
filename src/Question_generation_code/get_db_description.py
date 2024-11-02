import os
# os.environ["https_proxy"] = "http://localhost:10809"

from src.qa import makecomversation
import yaml
import json
import pandas as pd
from openai import APIConnectionError, OpenAI

import sqlite3

def extract_tables_and_columns(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    tables_info = {}
    for table in tables:
        table_name = table[0]
        try:
            cursor.execute("PRAGMA table_info({});".format(table_name))
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            continue 
        columns_info = cursor.fetchall()
        columns = [(col[1], col[2]) for col in columns_info]
        tables_info[table_name] = columns

    conn.close()

    structure_description = []
    for table_name, columns_info in tables_info.items():
        column_des = []
        for column_name, column_type in columns_info:
            des = f'{column_name}({column_type})'
            column_des.append(des)
        columns_info = ', '.join(column_des)
        table_strucure = f'Table {table_name} contains columns: {columns_info}'
        structure_description.append(table_strucure)

    return tables_info, structure_description

# db_file = './database/northwind.sqlite'
# tables_info, structure_description = extract_tables_and_columns(db_file)

# structure_description 


def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
config = load_config('config.yaml')


client = OpenAI(
    api_key=config['api']['key']
)

def get_table_descriptions(structure_info, db_description, table_indicators): ## from gpt
    prompt = f"""You are a database design expert. 
    You need to guess the meaning of the provided fields based on the provided database structure information and a description of the database.
    the database description is:
    {db_description}

    The database structure information is:
    {structure_info}
    """
    usercontent = f"""You need to guess the meaning of each field in the table provided below, and then add a description for each field separately. 
    Make sure there are no omissions.
    
    The table contains the following fields:
    {table_indicators}
    """
    
    return_format = '[{"table indicator": "the meaning of the indicator"}, {"table indicator": "the meaning of the indicator"}, ...]'
    
    result = makecomversation(prompt, usercontent, return_format)
    return result


with open('datasource.json', 'r',encoding='utf-8') as file:
        urls = json.load(file)

print(makecomversation(prompt='hello',usercontent='test',return_format=''))

results = {}
for item in urls:
    if 'description' not in item:
        print(f"database {item['db_name']} has no description, jump to next database")
        print(item)
        continue
    
    db_name = item['db_name']
    print(f"start to process {db_name}")
    db_file = os.path.join('./database/', f'{db_name}.sqlite')
    if not os.path.exists(db_file):
        print(f"database file {db_file} not exists, jump to next database")
        continue
    
    # 如果目录 f'./database_descriptions/' 该f'{db_name}_descriptions.csv' 已经存在了就跳过
    if os.path.exists(f'./database_descriptions/{db_name}_descriptions.csv'):
        print(f"database {db_name} description file already exists, jump to next database")
        continue

    tables_info, structure_description = extract_tables_and_columns(db_file)
    if not tables_info:
        print(f"database {db_name} extract tables and columns failed, jump to next database")
        continue

    table_descriptions = {}
    for table_name in tables_info:
        columns = tables_info[table_name]
        table_indicators = []
        for column in columns:
            indicator = f"{table_name}.{column[0]}"
            table_indicators.append(indicator)
        print(f"start to process table {table_name}, indicators: {table_indicators}")
        table_des,_,_ = get_table_descriptions(structure_description, item['description'], table_indicators)
        table_descriptions[table_name] = table_des
        
    
    table_list = []
    column_list = []
    description_list = []

    for table, columns in table_descriptions.items():
        # print(columns)
        # print(type(columns))
        for column, description in columns.items():
            # bug:??
            column = column.split('.')[-1]
            table_list.append(table)
            column_list.append(column)
            description_list.append(description)

    df = pd.DataFrame({
        'table': table_list,
        'column': column_list,
        'description': description_list
    })

    df.to_csv(f'./database_descriptions/{db_name}_descriptions.csv', index=False)