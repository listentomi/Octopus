import pandas as pd, re
from tqdm import tqdm
import sqlite3
import json
import os
import multiprocessing
import time
import sys


def get_connection(db_path):
    '''获取SQLite数据库连接'''
    connection = sqlite3.connect(db_path,timeout = 10)
    return connection

def execute_query(query,db_path):
    connection = get_connection(db_path)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        error_message = f"Query execution error: {e}"
        return "Error", error_message
    result = cursor.fetchmany(10)
    cursor.close()
    connection.close()
    return result

def connect_execute_query(query,db_path):
    '''连接数据库并执行查询'''
    connection = None
    cursor = None
    try:
        connection = get_connection(db_path)

        if connection is not None:
            pool = multiprocessing.Pool(processes=1)
            result = pool.apply_async(execute_query, (query,db_path))
            try:
                result.get(timeout=300)
            except multiprocessing.TimeoutError:
                pool.terminate()
                pool.join()
                return "Error", "Query execution timed out"
            else:
                pool.close()
                pool.join()
                return result.get()
            # cursor.timeout = 10  # Set the timeout value in seconds
            result = cursor.fetchmany(10)
            return result

    except sqlite3.Error as e:
        error_message = f"Database error: {e}"
        return "Error", error_message

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def fetch_query_results(db_path, query, batch_size=100):
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 执行查询
    cursor.execute(query)
    
    while True:
        # 分批获取查询结果
        results = cursor.fetchmany(batch_size)
        if not results:
            break
        yield results

    # 关闭连接
    conn.close()

def compare_results(generator1, generator2):
    # 比较结果集
    for batch1, batch2 in zip(generator1, generator2):
        if batch1 != batch2:
            return False
    return True

# Rest of the code remains the same
def compare_query_results(query1, query2, db_path):
    '''比较两个查询的结果是否相同'''
    print('query1:', query1)
    results1 = connect_execute_query(query1,db_path)
    print("results1:", results1)
    print('query2:', query2)
    results2 = connect_execute_query(query2,db_path)
    print("results2:", results2)
    if (len(results1) == 2 and results1[0] == "Error") or (len(results2) == 2 and results2[0] == "Error"):
        if (len(results1) == 2 and results1[0] == "Error") and (len(results2) == 2 and results2[0] == "Error"):
            # return "Error1,2", results1, results2
            return "Error1,2"
        elif (len(results1) == 2 and results1[0] == "Error") and not (len(results2) == 2 and results2[0] == "Error"):
            # return "Error1", results1, results2
            return "Error1"
        elif not (len(results1) == 2 and results1[0] == "Error") and (len(results2) == 2 and results2[0] == "Error"):
            # return "Error2", results1, results2
            return "Error2"
        # return "Error", results1, results2
        return "Error"
    if not results1 or not results2:
        if not results1 and not results2:
            # return "Empty1,2", results1, results2
            return "Empty1,2"
        elif not results1 and results2:
            # return "Empty1", results1, results2
            return "Empty1"
        elif results1 and not results2:
            # return "Empty2", results1, results2
            return "Empty2"
        # return results1, results2
        return "Empty"
    sorted_results1 = [tuple(sorted(str(item) for item in row)) for row in results1]
    sorted_results2 = [tuple(sorted(str(item) for item in row)) for row in results2]

    print("sorted_results1:", sorted_results1)
    print("sorted_results2:", sorted_results2)

    return sorted_results1 == sorted_results2
    # return results1 == results2



if __name__ == "__main__":

    db_dir = './test_databases'

    compare_file_1 = sys.argv[1]
    compare_file_2 = sys.argv[2]
    output_path = sys.argv[3]


    # 读取json文件
    with open(compare_file_1, 'r', encoding='utf-8') as file:
        data1 = json.load(file)

    with open(compare_file_2, 'r', encoding='utf-8') as file:
        data2 = json.load(file)

    print(len(data1), len(data2))
    assert len(data1) == len(data2), "两个文件中的SQL数量不一致"

    data_output = []
    correct_count = 0
    with tqdm(total=len(data1)) as pbar:
        for item1, item2 in zip(data1, data2):
            db_name1, sql1 = list(item1.items())[0]
            db_name2, sql2 = list(item2.items())[0]
            if db_name1 != db_name2:
                raise ValueError("两个文件中的数据库名称不一致") 
            result = compare_query_results(sql1, sql2, os.path.join(db_dir, f"{db_name1}.sqlite"))
            if result == True:
                correct_count += 1
            data_output.append({
                "db_name": db_name1,
                "gold_sql": sql1,
                "generated_sql": sql2,
                "result": result
            })
            pbar.update(1)
    # data_output写入json文件
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data_output, file, ensure_ascii=False, indent=4)
    print(f"正确率: {correct_count / len(data1)}")
