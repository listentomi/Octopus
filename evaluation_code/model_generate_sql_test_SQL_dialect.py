
from openai import OpenAI, RateLimitError
import os
import json
from tqdm import tqdm
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


# os.environ["https_proxy"] = "http://localhost:7890"
gpt35_api_key = "your key"
gpt4_api_key = "your key"
gpt35_url = "https://api.chatanywhere.tech/v1"
proxy_url = 'https://api.openai-proxy.com'
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=gpt4_api_key,
    # base_url=gpt35_url
)

total_tokens_used = 0
prompt_tokens_used = 0
output_tokens_used = 0

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

# 编写函数提取输入字符串中可能存在的列表对象
def extract_list_objects(input_string):
    # 从输入字符串中提取可能存在的列表对象
    list_objects = []
    # 从输入字符串中提取可能存在的列表对象
    
    for i in range(len(input_string)):
        if input_string[i] == '[':
            start = i
        if input_string[i] == ']':
            end = i
            try:
                list_objects.append(eval(input_string[start:end+1]))
            except:
                pass
    if len(list_objects) == 0:
        return None
    return list_objects[0]\

def batch_generate_by_LLM(question_list=[],type_list = [], function_list = [],  create_table_sql="", model_choice="gpt-4-0125-preview"):

    example_question_list = ["What are the employee numbers of department managers who are not part of any listed departments?",
                             "What are the birth dates of the employees who are not department managers?",
                             "How many end dates are there for employees who are not part of any listed department?"]
    example_sql_list = ["SELECT dm.emp_no FROM dept_manager dm LEFT JOIN departments d ON dm.dept_no = d.dept_no WHERE d.dept_no IS NULL;",
                        "SELECT e.birth_date FROM employees e LEFT JOIN dept_manager dm ON e.emp_no = dm.emp_no WHERE dm.emp_no IS NULL;",
                        "SELECT COUNT(*) FROM titles t LEFT JOIN employees e ON t.emp_no = e.emp_no WHERE e.emp_no IS NULL;"]

    messages = [
        {"role": "system", "content": f"Given the following SQL tables, your job is to write queries given a user’s request. \n\n{create_table_sql}"},
        {"role": "user","content": f'Write a SQL query for each question in the following question list:\n\n{example_question_list}\n\n Only return the all generated SQLs in one python list object like \n\n[generated_sql1,generated_sql2,generated_sql3,...]'},
        {"role": "assistant","content": f'{example_sql_list}'},
        {"role": "user","content": f'Write a SQL query for each question in the following question list:\n\n{question_list}\n\n Each SQL must be corresponding to the database system in order in the list {type_list} and use the function in order in the list {function_list}\n\nOnly return the generated SQLs in a list object like \n\n[generated_sql1,generated_sql2,generated_sql3,generated_sql4,...].'},
    ]
    completion = completion_with_backoff(model=model_choice, messages=messages,temperature=0.7, top_p=1)
    global total_tokens_used
    global prompt_tokens_used

    global output_tokens_used
    total_tokens_used+=completion.usage.total_tokens
    prompt_tokens_used+=completion.usage.prompt_tokens
    output_tokens_used+=completion.usage.completion_tokens
    print("one batch cost: ", completion.usage.total_tokens)
    response = completion.choices[0].message.content
    if extract_list_objects(response) and len(extract_list_objects(response))==len(question_list):
        return extract_list_objects(response)
    else:
        max_retry = 3
        retry_count = 0
        while (not extract_list_objects(response)) or len(extract_list_objects(response))<len(question_list):
            print("retrying...")
            if retry_count>max_retry:
                break
            completion = completion_with_backoff(model=model_choice, messages=messages,temperature=1, top_p=1)
            total_tokens_used+=completion.usage.total_tokens
            prompt_tokens_used+=completion.usage.prompt_tokens
            output_tokens_used+=completion.usage.completion_tokens
            print("one batch cost: ", completion.usage.total_tokens)
            response = completion.choices[0].message.content
            print(response)
            if extract_list_objects(response) and len(extract_list_objects(response))==len(question_list):
                return extract_list_objects(response)
            retry_count+=1
        print("Failed to generate SQLs for this batch, please check the question list.")
        return question_list

def main():
    batch_size = 1

    database_info_path = '.\\test\\test_databases_create_info'
    output_sql_path = '.\\test\\test_generated_sqls_gpt35_SQL_dialect.json'
    
    with open(".\\test\\test_SQL_dialect_diversity_for_generative.json", "r",encoding='utf-8') as f:
        data = json.load(f)

    for db_name, db_entries in data.items():
        print(f"Database Name: {db_name}")
        current_db_question_list = []
        type_list = []
        function_list = []
        for entry in db_entries:
            current_db_question_list.append(entry['question'])
            type_list.append(entry['type'])
            function_list.append(entry['function'])
        # print(current_db_question_list)

        # 根据batch_size分批遍历问题列表
        with tqdm(total=len(current_db_question_list), desc="Generating SQLs") as pbar:
            for i in range(0, len(current_db_question_list), batch_size):
                batch_question_list = current_db_question_list[i:i+batch_size]
                batch_type_list = type_list[i:i+batch_size]
                batch_function_list = function_list[i:i+batch_size]
                pbar.update(len(batch_question_list))
                # 以字符串形式读取指定路径的.sql文件
                with open(os.path.join(database_info_path,f"{db_name}_create.sql"), "r") as f:
                    create_table_sql = f.read()
                batch_generated_SQLs_list=batch_generate_by_LLM(batch_question_list,batch_type_list,batch_function_list, create_table_sql,model_choice='gpt-3.5-turbo-0125')
                # 将batch_generated_SQLs_list的元素添加到generated_SQLs_list中
                if batch_generated_SQLs_list:
                    for sql in batch_generated_SQLs_list:
                        if not os.path.exists(output_sql_path):
                            with open(output_sql_path, 'w', encoding='utf-8') as f:
                                json.dump([{db_name:sql}],f,ensure_ascii=False,indent=4)
                        # 如果output_sql_path文件存在，则将json对象列表续写入文件
                        else:
                            with open(output_sql_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            data.append({db_name:sql})
                            with open(output_sql_path, 'w', encoding='utf-8') as f:
                                json.dump(data,f,ensure_ascii=False,indent=4)
                time.sleep(1)
    return 

if __name__=='__main__':
    main()