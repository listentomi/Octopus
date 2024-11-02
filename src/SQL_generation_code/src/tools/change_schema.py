import json
import os
import sys
# 读取 generative_schema.json 文件
input_folder_path = sys.argv[1]
with open(os.path.join(input_folder_path,'generative','origin_schema.json'), 'r') as file:
    data = json.load(file)

# 在每条数据中添加新列
for item in data:
    #item['math_ops_columns'] = {'+': [], '-': [], '*': [], '/': []}

    # 获取所有 "original_datatype" 为 "number" 的 "name" 列表
    number_columns = [column['name'] for column in item['columns'] if column['original_datatype'] == 'number']
    # 为 '+', '-', '*', '/' 的值赋值为 number_columns 列表
    if len(number_columns) != 0:
        item['math_ops_columns'] = {'+': [], '-': [], '*': [], '/': []}
        item['math_ops_columns']['+'] = number_columns
        item['math_ops_columns']['-'] = number_columns
        item['math_ops_columns']['*'] = number_columns
        item['math_ops_columns']['/'] = number_columns

# 将更新后的数据写入新的文件 schema.json
with open(os.path.join(input_folder_path,'generative','schema.json'), 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
