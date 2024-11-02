import os
# os.environ["https_proxy"] = "http://localhost:10809"

import subprocess
import argparse
import requests
from bs4 import BeautifulSoup
import json


def main(data_dir,results_dir,json_sql_indicator='sql', batchsize=10, final_batch=False):
    os.makedirs(results_dir, exist_ok=True)
    for root, dirs, files in os.walk(data_dir):
        # 构造目标文件夹路径
        new_folder = os.path.join(results_dir, os.path.relpath(root, data_dir))
        os.makedirs(new_folder, exist_ok=True)
        data_forder = os.path.join(data_dir, os.path.relpath(root, data_dir))
        # 遍历目录下所有文件
        for filename in os.listdir(data_forder):
            print(filename)
            file_path = os.path.join(data_forder, filename)
            print(file_path)
            if os.path.isfile(file_path):
                # 提取文件名（不含扩展名）
                filename_no_ext = os.path.splitext(filename)[0]
                print(filename_no_ext)
                # 执行 Python 脚本
                output_path = os.path.join(new_folder, f"{filename_no_ext}.json")
                print(output_path)
                subprocess.run(["python", "sql2question_batch.py", "--sql_path", file_path, "--output_path", output_path, "--json_sql_indicator", json_sql_indicator, "--batchsize", str(batchsize), "--final_batch", str(final_batch)])


def get_descriptions_from_url():
    with open('datasource.json', 'r') as file:
        urls = json.load(file)

    for item in urls:
        url = item['url']
        db_name = item['db_name']

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        ld_json_tags = soup.find_all('script', type='application/ld+json')
        tags = json.loads(ld_json_tags[0].text.strip())
        descriptions = tags['description']
        item['description'] = descriptions


    with open('datasource.json', 'w') as file:
        json.dump(urls, file, indent=4)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='SQL to question translation')

    # random seed
    parser.add_argument('--input_path', type=str, default='./data/3_21/', help='输入文件根目录')
    parser.add_argument('--output_path', type=str, default='./results/3_21/json/', help='结果输出文件根目录')
    parser.add_argument('--json_sql_indicator', type=str, default='sql', help='json文件的sql语句的key')
    parser.add_argument('--batchsize', type=int, default=10, help='一组翻译的sql的数量')
    parser.add_argument('--final_batch', type=bool, default=False, help='是否在最后翻译过程中使用batch')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    json_sql_indicator = args.json_sql_indicator
    batchsize = args.batchsize
    final_batch = args.final_batch
    main(input_path,output_path,json_sql_indicator, batchsize, final_batch)
