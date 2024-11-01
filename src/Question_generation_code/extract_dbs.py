import os
import shutil

# Define the directory where your subfolders are located
base_directory = "E:\\benchmark_databases\\new_spiderdbs"  # Replace with the path to your directory

# Define the new directory where the .sqlite files will be placed
new_directory = "D:\BaiduNetdiskWorkspace\横向\哈工深合作text2sql\问题生成代码最新版\sql2nl\databases"
new_directory_path = os.path.join(base_directory, new_directory)

# Create the new directory if it doesn't exist
if not os.path.exists(new_directory_path):
    os.makedirs(new_directory_path)

# Walk through the base directory
for subdir, dirs, files in os.walk(base_directory):
    for file in files:
        if file.endswith(".sqlite"):
            # Construct the full file path
            file_path = os.path.join(subdir, file)
            # Construct the destination path
            destination = os.path.join(new_directory_path, file)
            # Copy the file to the new directory
            shutil.copy(file_path, destination)
            print(f"Copied: {file} to {new_directory_path}")

print("All .sqlite files have been copied to the new directory.")