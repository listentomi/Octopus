import json
import os

# 定义根文件夹路径
root_folder_path = './data'
output_file_path = './merged_synthetic_queries.json'

def find_synthetic_queries_files(root_path):
    synthetic_queries_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename == 'synthetic_queries.json':
                synthetic_queries_files.append(os.path.join(dirpath, filename))
    return synthetic_queries_files

def merge_json_files(file_paths, output_path):
    merged_data = []
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            merged_data.extend(data)
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, indent=4, ensure_ascii=False)
    
    print(f"Merged JSON data has been saved to {output_path}")

# 查找所有 synthetic_queries.json 文件
synthetic_queries_files = find_synthetic_queries_files(root_folder_path)

# 调用函数进行合并
merge_json_files(synthetic_queries_files, output_file_path)
