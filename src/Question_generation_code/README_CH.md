# sql转自然语言问题

使用的主要工具为Openai api和sql解析工具sqlsparse，通过多轮问答和sql分解的方法，将sql语句转换为自然语言问题。

## 1. 环境安装和配置
1. 安装环境 
  ```shell
pip install -r requirements.txt
```
2. 环境变量配置
在config.yaml 文件中配置openai api key


## 2. 英文翻译
### 1. 翻译单个文件

主要文件为sql2question_parallel.py，其中包含了多轮问答和sql解析的方法，将sql语句转换为英文问题。调用命令：
```shell
 python sql2question_parallel.py --sql_path sakila_sqls.json --output_path new_sakila.json --json_sql_indicator query
```
其中
`---sql_path`: 输入文件
`---output_path`: 输出文件
`---json_sql_indicator`: json文件中sql语句的key值

### 2. 批量翻译
批处理脚本sql2nl_batch.py 对指定文件夹下的所有json文件进行处理，将sql语句转换为自然语言问题。
```shell
 python sql2nl_batch.py --input_path ./data/3_21/ --output_path ./result/3_21/json/ --json_sql_indicator query
 ```
其中
`---input_path`: 输入文件夹
`---output_path`: 输出文件夹
`---json_sql_indicator`: json文件中sql语句的key值


## 3. 英文到中文翻译
### 1. 翻译单个文件
主要文件为en2ch.py，其中包含了多轮问答和sql解析的方法，将英文问题转换为中文问题。调用命令：
```shell
 python en2ch.py --input_path ./result/3_21/json/ --output_path ./result/3_21/ch_json/ 
```
其中
`---sql_path`: 输入文件
`---output_path`: 输出文件



### 2. 批量翻译
批处理脚本en2ch_batch.py 对指定文件夹下的所有json文件进行处理，将sql语句转换为自然语言问题，并将结果保存到指定文件夹。
```shell
 python en2ch_batch.py --input_path ./data/3_21/ --output_path ./result/3_21/json/ 
 ```
其中
`---input_path`: 输入文件夹
`---output_path`: 输出文件夹


