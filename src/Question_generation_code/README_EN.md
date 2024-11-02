# Generate questions

## generate database descriptions

1. put .sqlite databases in the directory `.\database`
2. run `fill_newdb_to_datasource.py`
   
   ```
   python fill_newdb_to_datasource.py 
   ```
3. run `get_db_description.py`
   
   ```
   python get_db_description.py 
   ```
   
   ## generate quetions for sqls
4. collect generated sqls in a .json file named by the database name, if there are generated sqls for multiple databases, put .json files split by database name into a directory
5. for single .json file, run `sql2question_parallel.py`
   
   ```shell
   python sql2question_parallel.py --sql_path sakila_sqls.json --output_path new_sakila.json --json_sql_indicator query
   ```
   
   其中
   `---sql_path`: 输入文件
   `---output_path`: 输出文件
   `---json_sql_indicator`: json文件中sql语句的key值
6. for multiple .json files, run `sql2nl_batch.py `
   
   ```shell
   python sql2nl_batch.py --input_path ./data/3_21/ --output_path ./result/3_21/json/ --json_sql_indicator readable_query
   ```
   
   其中
   `---input_path`: 输入文件夹
   `---output_path`: 输出文件夹
   `---json_sql_indicator`: json文件中sql语句的key值