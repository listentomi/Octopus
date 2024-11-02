import mysql.connector
import pandas as pd
import re
import numpy as np

database = 'voc'
def connect_db():
    # object to hold the connection
    mydb = None
    try:
        # connection parameters
        # mydb = mysql.connector.connect(
        #     host = 'localhost',
        #     user = 'root',
        #     password = '111111',
        #     database = database
        # )
        mydb = mysql.connector.connect(
            host = 'db.relational-data.org',
            user = 'guest',
            password = 'relational',
            database = database
        )
    except Exception as e:
        print('Error: ', e)
    return mydb

def run_query(mydb, query):
    # object to hold the cursor
    cursor = mydb.cursor()
    try:
        # execute the query
        cursor.execute(query)
        # fetch all the rows
        rows = cursor.fetchall()
        # get the column names
        col_names = [i[0] for i in cursor.description]
        # create a pandas dataframe from the rows
        df = pd.DataFrame(rows, columns=col_names)
        return df
    except Exception as e:
        print('Error: ', e)
    finally:
        # close the cursor
        cursor.close()

# connect to the database
mydb = connect_db()

# your sql queries
query1 = """
SELECT
    A.TABLE_NAME 'table_names',
    A.TABLE_NAME 'table_names_original',
    A.COLUMN_NAME 'column_names',
    A.COLUMN_NAME 'column_names_original',
    A.DATA_TYPE 'column_types',
    A.COLUMN_COMMENT 'column_comment',
    B.CONSTRAINT_NAME 'primary_key_name'
FROM INFORMATION_SCHEMA.COLUMNS A
LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE B
ON A.TABLE_SCHEMA = B.TABLE_SCHEMA
AND A.TABLE_NAME = B.TABLE_NAME
AND A.COLUMN_NAME = B.COLUMN_NAME
WHERE A.TABLE_SCHEMA='{database}'
ORDER BY A.TABLE_SCHEMA, A.TABLE_NAME, A.ORDINAL_POSITION;
""".format(database=database)

query2 = """
SELECT
    KCU.TABLE_NAME 'origin_table',
    KCU.COLUMN_NAME 'origin_column',
    KCU.REFERENCED_TABLE_NAME 'referenced_table_name',
    KCU.REFERENCED_COLUMN_NAME 'referenced_column_name'
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU
WHERE KCU.TABLE_SCHEMA='{database}'
AND KCU.REFERENCED_TABLE_NAME IS NOT NULL;
""".format(database=database)


df1 = run_query(mydb, query1)
df2 = run_query(mydb, query2)
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
df.to_excel(f'{database}.xlsx', index=False)
