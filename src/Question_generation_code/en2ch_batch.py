import os
import subprocess
import argparse

def main(data_dir,results_dir):
    os.makedirs(results_dir, exist_ok=True)
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
                output_path = os.path.join(new_folder, f"{filename_no_ext}.json")
                subprocess.run(["python", "en2ch.py", "--sql_path", file_path, "--output_path", output_path])
   

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='SQL to question translation')

    parser.add_argument('--input_path', type=str, default='./data/3_21/', help='输入文件目录')
    parser.add_argument('--output_path', type=str, default='./results/3_21/json/', help='结果输出文件目录')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path

    main(input_path,output_path)
