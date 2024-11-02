import os
import subprocess
import argparse

def main(data_dir,results_dir,json_sql_indicator='sql'):
    os.makedirs(results_dir, exist_ok=True)
    for root, dirs, files in os.walk(data_dir):
        # 构造目标文件夹路径
        new_folder = os.path.join(results_dir, os.path.relpath(root, data_dir))
        os.makedirs(new_folder, exist_ok=True)
        data_forder = os.path.join(data_dir, os.path.relpath(root, data_dir))
        # 遍历目录下所有文件
        for filename in os.listdir(data_forder):
            file_path = os.path.join(data_forder, filename)
            if os.path.isfile(file_path):
                # 提取文件名（不含扩展名）
                filename_no_ext = os.path.splitext(filename)[0]
                # 执行 Python 脚本
                output_path = os.path.join(results_dir, f"{filename_no_ext}.json")
                subprocess.run(["python", "sql2question_parallel.py", "--sql_path", file_path, "--output_path", output_path, "--json_sql_indicator", json_sql_indicator])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='SQL to question translation')

    # random seed
    parser.add_argument('--input_path', type=str, default='./data/3_21/', help='输入文件根目录')
    parser.add_argument('--output_path', type=str, default='./results/3_21/json/', help='结果输出文件根目录')
    parser.add_argument('--json_sql_indicator', type=str, default='sql', help='json文件的sql语句的key')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    json_sql_indicator = args.json_sql_indicator

    main(input_path,output_path,json_sql_indicator)