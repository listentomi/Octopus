import pandas as pd
import json
import re
import os
import sys
import shutil

# 获取指定文件夹中的所有xlsx文件路径
folder_path = sys.argv[1]
db_folder_path = sys.argv[2]
xlsx_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
# 提取xlsx文件名
xlsx_files_name = [os.path.splitext(file)[0] for file in xlsx_files]
print(xlsx_files_name)
# 遍历所有xlsx文件
for file,file_name in zip(xlsx_files,xlsx_files_name):
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)

    pattern = '[^\w]'
    database = re.sub(pattern, '_', file_name)
    
    # 根据 table_names 列进行分组，并将 column_names 列转换为列表
    grouped = df.groupby('table_names')['column_names'].apply(list).reset_index()
    # 准备存储所有数据的列表
    all_column_names = []

    # 将所有 "column_names" 列合并到一个列表中，并在每个子列表前添加对应的数字
    for idx, row in grouped.iterrows():
        table_name = row['table_names']
        column_names = row['column_names']
        all_column_names.extend([[idx, col] for col in column_names])  # 添加对应的数字到每个子列表
    # 在所有数据前面添加一个 [-1, "*"]
    all_column_names.insert(0, [-1, "*"])
    # 将数据放入字典中
    data_dict = {"column_names": all_column_names}

    # 添加 "column_names_original" 列
    data_dict["column_names_original"] = all_column_names

    # 添加 "column_types" 列并在最前面添加空字符串元素
    column_types = df["column_types"].tolist()
    column_types.insert(0, "")
    data_dict["column_types"] = column_types

    # 添加 "db_id" 列
    data_dict["db_id"] = f"{database}"

    # 生成 "primary_keys" 列
    primary_keys = []
    for idx, row in df.iterrows():
        if row['primary_key_name'] == 'PRIMARY':
            primary_keys.append(idx + 1)
    data_dict["primary_keys"] = primary_keys

    # 生成 "foreign_keys" 列
    foreign_keys = []
    for idx, row in df.iterrows():
        origin_table = row['origin_table']
        origin_column = row['origin_column']
        referenced_table_name = row['referenced_table_name']
        referenced_column_name = row['referenced_column_name']
        
        # 查找 origin_table 和 origin_column 在当前行的索引列表
        origin_indexes = df[(df['table_names'] == origin_table) & (df['column_names'] == origin_column)].index.tolist()
        
        # 查找 referenced_table_name 和 referenced_column_name 在当前行的索引列表
        referenced_indexes = df[(df['table_names'] == referenced_table_name) & (df['column_names'] == referenced_column_name)].index.tolist()
        
        # 确保列表不为空
        if origin_indexes and referenced_indexes:
            # 获取第一个索引值
            origin_index = origin_indexes[0] + 1
            referenced_index = referenced_indexes[0] + 1
            
            foreign_keys.append([origin_index, referenced_index])

    data_dict["foreign_keys"] = foreign_keys

    # 添加 "table_names" 列并去重
    table_names = df["table_names"].tolist()
    unique_table_names = []
    [unique_table_names.append(x) for x in table_names if x not in unique_table_names]

    # 添加 "table_names_original" 列并去重
    data_dict["table_names"] = unique_table_names
    data_dict["table_names_original"] = unique_table_names

    # 将字典放入列表中
    data_list = [data_dict]

    # 调整字典中键值对的顺序
    ordered_keys = ["column_names", "column_names_original", "column_types", "db_id", "primary_keys", "foreign_keys", "table_names", "table_names_original"]
    ordered_data_dict = {key: data_dict[key] for key in ordered_keys}

    # 如果不存在创建新文件夹，以xslx文件名命名
    output_folder = os.path.join(os.getcwd(), 'data',file_name)
    print(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    
    # 将列表转换为 JSON 格式并写入文件
    json_data = json.dumps([ordered_data_dict], indent=2)
    with open(os.path.join(output_folder, 'tables.json'), 'w') as f:
        f.write(json_data)

    # 将db_folder_path中同名数据库文件移动到output_folder,并删除原始数据库文件
    source_db_file = os.path.join(db_folder_path, f"{database}.db")
    target_db_file = os.path.join(output_folder, f"{database}.db")
    shutil.move(source_db_file, target_db_file)

    # 删除db_folder_path
    shutil.rmtree(db_folder_path)
   