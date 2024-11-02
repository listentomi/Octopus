#!/bin/bash

# 获取第一个命令行参数作为文件夹路径
folder_path=$1

# 遍历文件夹下的所有子文件夹
for subdir in "$folder_path"/*; do
    # 检查是否为文件夹
    if [ -d "$subdir" ]; then
        # 输出子文件夹路径
        # echo "$subdir"
        # 提取最后文件名
        subdir_name=$(basename "$subdir")
        # 输出最后文件名
        echo "processing $subdir_name"
        
        # 判断subdir路径下子文件夹generative中origin_schema.json是否存在
        if [ -f "$subdir/generative/origin_schema.json" ]; then
            # 输出子文件夹路径
            echo "$subdir/generative/origin_schema.json exists"
        else
            # 输出子文件夹路径
            # echo "$subdir/generative/origin_schema.json does not exist"
            # 执行python命令，将子文件夹路径作为参数
            python src/tools/transform_generative_schema.py --db_path "$subdir_name"
        fi

        # 判断subdir路径下子文件夹generative中schema.json是否存在
        if [ -f "$subdir/generative/schema.json" ]; then
            # 输出子文件夹路径
            echo "$subdir/generative/schema.json exists"
        else
            # 输出子文件夹路径
            # echo "$subdir/generative/schema.json does not exist"
            # 执行python命令，将子文件夹路径作为参数
            python src/tools/change_schema.py "$subdir"
        fi

        # 判断subdir路径下子文件夹generative中generative_schema.json是否存在
        if [ -f "$subdir/generative/generative_schema.json" ]; then
            # 输出子文件夹路径
            echo "$subdir/generative/generative_schema.json exists"
        else
            # 输出子文件夹路径
            # echo "$subdir/generative/generative_schema.json does not exist"
            # 执行python命令，将子文件夹路径作为参数
            python src/tools/change_schema2.py "$subdir"
        fi
    fi
done