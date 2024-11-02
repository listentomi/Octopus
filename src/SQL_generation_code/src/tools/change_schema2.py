import json
import os
import sys
# 读取 generative_schema.json 文件
input_folder_path = sys.argv[1]
with open(os.path.join(input_folder_path,'generative','schema.json'), 'r') as file:
    data = json.load(file)

res = {'+': {}, '-': {}, '*': {}, '/': {}}
# 处理每个数据
for item in data:
    if 'math_ops_columns' in item:
        math_ops_columns = item['math_ops_columns']
        for operator in ['+', '-', '*', '/']:
            if operator in math_ops_columns:
                name = item['name']
                value = math_ops_columns[operator]
                res[operator][name] = value

# 在满足条件的情况下，在每个 "columns" 列表中的每个字典中添加新列
for item in data:
    for column in item['columns']:
        if column['original_datatype'] == 'number':
            res = {'+': {}, '-': {}, '*': {}, '/': {}}
            # 处理每个数据
            for item in data:
                if 'math_ops_columns' in item:
                    math_ops_columns = item['math_ops_columns']
                    for operator in ['+', '-', '*', '/']:
                        if operator in math_ops_columns:
                            name = item['name']
                            value = math_ops_columns[operator]
                            res[operator][name] = list(set(value) - set(column['name']))
            column['math_operands'] = res


# 将更新后的数据写入新的文件 schema.json
with open(os.path.join(input_folder_path,'generative','generative_schema.json'), 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

