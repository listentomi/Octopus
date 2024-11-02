import argparse
import json
import sys
import os

# 将当前工作目录添加到 Python 模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
# 获取父目录路径
parent_dir = os.path.dirname(current_dir)
# 将父目录路径添加到 Python 模块搜索路径
sys.path.append(parent_dir)
#from named_entity_recognition.api_ner.google_api_repository import remote_named_entity_recognition
from api_ner.google_api_repository import remote_named_entity_recognition

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--data_path', type=str, required=True)
    arg_parser.add_argument('--output_path', type=str, required=True)
    arg_parser.add_argument('--ner_api_secret', type=str, required=True)

    args = arg_parser.parse_args()

    with open(os.path.join(args.data_path), 'r') as json_file:
        data = json.load(json_file)

    error_count = 0
    flag = 0
    ner_data = []
    for doc in data:
        flag = flag + 1
        extracted_values = remote_named_entity_recognition(doc['question'], args.ner_api_secret)
        if extracted_values:
            ner_data.append({
                'entities': extracted_values['entities'],
                'language': extracted_values['language'],
                'question': doc['question']
            })
        else:
            error_count += 1

        if(flag % 50 == 0):
            with open(os.path.join(args.output_path), 'w', encoding='utf-8') as f:
                json.dump(ner_data, f, ensure_ascii=False, indent=2)
    # with open(os.path.join(args.output_path), 'w', encoding='utf-8') as f:
    #     json.dump(ner_data, f, ensure_ascii=False, indent=2)

    print("Extracted {} values. {} requests failed.".format(len(data), error_count))
