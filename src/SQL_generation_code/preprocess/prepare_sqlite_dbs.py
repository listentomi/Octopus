import os
import shutil
import argparse
from pathlib import Path


def find_and_copy_sqlite_files(source_folder, target_folder):
    # 检查target_folder文件夹是否是source_folder子文件夹，如果是则报错
    if target_folder in source_folder.parents:
        raise ValueError("The target folder cannot be a subfolder of the source folder.")
    # 遍历source_folder下的所有文件,包括嵌套子文件夹, 找到所有的sqlite文件, 并将其复制到target_folder下,后缀修改成.db
    if not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".sqlite"):
                source_file = Path(root) / file
                target_file = target_folder / (file.rsplit(".", 1)[0] + ".db")
                shutil.copy2(source_file, target_file)
    
    # # Get the list of files in the source folder
    # files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    # # Get the list of subfolders in the source folder
    # subfolders = [f for f in os.listdir(target_folder) if os.path.isdir(os.path.join(target_folder, f))]

    # for subfolder in subfolders:
    #     # Construct the paths for the source and target db files
    #     source_db_file = os.path.join(source_folder, subfolder + '.db')
    #     target_db_file = os.path.join(target_folder, subfolder, subfolder + '.db')

    #     # Copy the db file to the target folder
    #     shutil.copyfile(source_db_file, target_db_file)

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder', help='Path to the folder containing db files')
    parser.add_argument('target_folder', help='Path to the folder containing subfolders for each db file')
    args = parser.parse_args()

    # Call the function to copy the db files
    find_and_copy_sqlite_files(Path(args.source_folder), Path(args.target_folder))