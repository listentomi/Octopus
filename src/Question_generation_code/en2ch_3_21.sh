#!/bin/bash

for filename in ./results/3_21/json/*; do
    # 检查文件是否是普通文件
    if [ -f "$filename" ]; then
        # 提取文件名（不含路径）
        base=$(basename "$filename")
        # 提取文件名（不含扩展名）
        filename_no_ext="${base%.*}"
        # 执行 Python 脚本
        python en2ch.py --sql_path "$filename" --output_path "./results/3_21/ch/$filename_no_ext.json" 
    fi
done