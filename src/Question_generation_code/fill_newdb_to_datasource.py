import os
import json

# 指定要遍历的文件夹路径
directory = ".\database"  # 替换为实际的文件夹路径

# 指定JSON文件路径
json_file_path = '.\datasource.json'

# 尝试读取现有的JSON文件，如果文件不存在，则初始化为空列表
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        databases_info = json.load(file)
except FileNotFoundError:
    databases_info = []

# 遍历文件夹
for filename in os.listdir(directory):
    if filename.endswith(".sqlite"):
        # 提取不包括扩展名的文件名
        db_name = os.path.splitext(filename)[0]
        # 创建符合指定格式的字典
        db_info = {
            "db_name": db_name,
            "url": "",
            "description": ""
        }
        # 将字典添加到列表中
        databases_info.append(db_info)

# 将更新后的列表写入JSON文件
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(databases_info, file, ensure_ascii=False, indent=4)

print("datasource.json has been updated with the new database information.")