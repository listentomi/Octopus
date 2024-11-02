
from openai import OpenAI, RateLimitError
import os
import json
from tqdm import tqdm
import time
import os
import datetime
import argparse
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


# os.environ["https_proxy"] = "http://localhost:10809"
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

# completion_with_backoff(model="text-davinci-003", prompt="Once upon a time,")

def extract_json_objects(text):
    json_objects = []
    stack = []  # 用于跟踪括号的栈
    start_index = -1  # 记录当前JSON对象开始的索引
    in_string = False  # 跟踪是否在字符串内

    for i, char in enumerate(text):
        if char == '"' and (i == 0 or text[i-1] != '\\'):
            in_string = not in_string  # 当我们遇到非转义的引号时，翻转in_string状态

        if in_string:
            continue  # 如果我们在字符串内部，不对括号做处理

        if char == '{':
            stack.append(char)
            if len(stack) == 1:
                # 我们可能遇到了一个新的JSON对象
                start_index = i
        elif char == '}':
            if stack:
                stack.pop()
                if len(stack) == 0:
                    # 栈为空，意味着我们完成了一个JSON对象的提取
                    end_index = i + 1  # '+1' 包含当前的闭括号
                    try:
                        # 截取字符串并尝试解析为JSON
                        obj_str = text[start_index:end_index]
                        obj = json.loads(obj_str)
                        json_objects.append(obj)
                    except json.JSONDecodeError as e:
                        print(f"JSON 解析错误位于 {start_index}-{end_index}: {e}")
                    start_index = -1
    
    if stack:
        # 如果栈不为空，意味着有未闭合的括号
        print("警告: 字符串中有未闭合的大括号")

    return json_objects

def read_file(file_path):
    """
    Reads the contents of a file.

    Args:
        file_path (str): The path of the file to be read.

    Returns:
        str: The contents of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    except IOError as e:
        raise IOError(f"Error reading the file '{file_path}': {str(e)}")

# 非流式响应
def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)

def gpt_35_api_stream(messages: list):

    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    
def score_by_llm(question="question", sql='sql', model_choice="gpt-3.5-turbo"):
    """
    Scores the given question-SQL pair using a language model.

    Args:
        question (str): The question to be scored.
        sql (str): The SQL query to be scored.
        model_choice (str): The choice of language model to use for scoring.

    Returns:
        dict: A dictionary containing the scores for question quality, SQL quality, consistency, and significance.
            The scores are in the range of 0 to 100.

    Example:
        >>> score_by_llm("What is the capital of France?", "SELECT capital FROM countries WHERE name = 'France'")
        {'question_quality': 85, 'SQL_quality': 90, 'consistency': 80, 'significance': 95}
    """
    
    # Function implementation goes here
    # 定义评分格式prompt
    example_schema = {
        "properties": {
            "foo": {
                "title": "Foo",
                "description": "a list of strings",
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["foo"]
    }
    well_formatted_object = {"foo": ["bar", "baz"]}
    not_well_formatted_object = {"properties": {"foo": ["bar", "baz"]}}
    # 定义评分json格式和评分指标
    my_score_metrics = {
        "properties": {
            "question_quality": {
                "title": "question_quality",
                "description": "question quality score in the range of 0 to 100",
                "type": "integer"
            },
            "SQL_quality": {
                "title": "SQL_quality",
                "description": "SQL quality score in the range of 0 to 100",
                "type": "integer"
            },
            "consistency": {
                "title": "consistency",
                "description": "consistency of question and SQL score in the range of 0 to 100",
                "type": "integer"
            },
            "significance": {
                "title": "significance",
                "description": "SQL query significance score in the range of 0 to 100",
                "type": "integer"
            }
        },
        "required": ["question_quality", "SQL_quality", "consistency", "significance"]
    }
    # prompt = f"""The output should be formatted as a JSON instance that conforms to the JSON schema below.\nAs an example, for the schema {example_schema} the object {well_formatted_object} is a well-formatted instance of the schema. The object {not_well_formatted_object} is not well-formatted.\nHere is the output schema: {my_score_metrics}\nScore the following question-SQL pair generated on a continuous scale from 0 to 100.\nQuestion: {question}\nSQL: {sql}"""
    # 定义模型输入的prompt，结合生成的question和sql
    prompt = (
        f"The output should be formatted as a JSON instance that conforms to the JSON schema below.\n"
        f"As an example, for the schema {example_schema}, the object {well_formatted_object} is a well-formatted instance of the schema. "
        f"The object {not_well_formatted_object} is not well-formatted.\n"
        f"Here is the output schema: {my_score_metrics}\n"
        f"Score the following question-SQL pair generated on a continuous scale from 0 to 100.\n"
        f"Question: {question}\n"
        f"SQL: {sql}"
    )
    messages = [
        {"role": "system", "content": "You are a SQL expert."},
        {"role": "user", "content": f"{prompt}"},
    ]
    try_count = 0
    while True:
        if try_count > 5:
            tqdm.write("Failed to get response after 5 tries.")
            response = {'error':'fail to get response after 5 tries'}
            return
        try:
            # 尝试发送请求
            completion = client.chat.completions.create(model=model_choice, messages=messages)
            response = completion.choices[0].message.content
            if response:
                break
        except RateLimitError:
            # 如果收到RateLimitError，等待一段时间然后再试
            tqdm.write("Rate limit exceeded, sleeping...")
            time.sleep(10)
            try_count += 1
    
    # print(response)
    # 将response转换为json格式
    # 添加异常处理
    try:
        response = json.loads(response)
    except Exception as e:
        tqdm.write(f"An error occurred: {e}")
        tqdm.write("Response: " + str(response))
        response = {'error':'error decoding JSON response'}
    # print(type(response))
    return response
    
def test_score_by_gpt4(question="question", sql='sql', model_choice="gpt-4"):
    """
    Scores the given question-SQL pair using a language model.

    Args:
        question (str): The question to be scored.
        sql (str): The SQL query to be scored.
        model_choice (str): The choice of language model to use for scoring.

    Returns:
        dict: A dictionary containing the scores for question quality, SQL quality, consistency, and significance.
            The scores are in the range of 0 to 100.

    Example:
        >>> score_by_llm("What is the capital of France?", "SELECT capital FROM countries WHERE name = 'France'")
        {'question_quality': 85, 'SQL_quality': 90, 'consistency': 80, 'significance': 95}
    """
    
    # Function implementation goes here
    # 定义评分格式prompt
    example_schema = {
        "properties": {
            "foo": {
                "title": "Foo",
                "description": "a list of strings",
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["foo"]
    }
    well_formatted_object = {"foo": ["bar", "baz"]}
    not_well_formatted_object = {"properties": {"foo": ["bar", "baz"]}}
    # 定义评分json格式和评分指标
    my_score_metrics = {
        "properties": {
            "question_quality": {
                "title": "question_quality",
                "description": "question quality score in the range of 0 to 100, the higher the better",
                "type": "integer"
            },
            "SQL_quality": {
                "title": "SQL_quality",
                "description": "SQL quality score in the range of 0 to 100, the higher the better",
                "type": "integer"
            },
            "consistency": {
                "title": "consistency",
                "description": "consistency of question and SQL score in the range of 0 to 100, the higher the better",
                "type": "integer"
            },
            "significance": {
                "title": "significance",
                "description": "SQL query significance score in the range of 0 to 100, the higher the better",
                "type": "integer"
            }
        },
        "required": ["question_quality", "SQL_quality", "consistency", "significance"]
    }

    criteria_prompt = (
        "Based on the following question-SQL pair, rate 'question_quality', 'SQL_quality', 'consistency', and 'significance' "
        "on a scale from 0 to 100. The scores should closely align with the following expectations:\n\n"
        "- 'question_quality' should reflect the clarity and fluency of the question and how relevant it is to potential users.\n"
        "- 'SQL_quality' should reflect the correctness of the SQL query in terms of syntax and its ability to retrieve the correct data as per the question.\n"
        "- 'consistency' should reflect how closely the SQL query matches the intention of the question.\n"
        "- 'significance' should reflect how likely the query is to be posed by real users and how informative and meaningful the results of the SQL query are.\n\n"
    )

    rate_qa_prompt = (
        f"Question: {question}\n"
        f"SQL: {sql}\n\n"
    )

    
    question1 = (
        "Based on above guidelines, provide the scores for each criterion in a JSON format. Here is the question-SQL pair:\n\n"
        f"Question: What is the average number of Mubi users who love movies directed by Stanley Kubrick?\n"
        f"SQL: SELECT AVG(movie_popularity) FROM movies WHERE director_name = 'Stanley Kubrick'\n\n"
    )
    
    answer1 = """{
        "question_quality": {
            "score": 90, 
            "rationale": "The question is clear and fluent, and it is relevant to potential users, especially those interested in Stanley Kubrick's movies or movie popularity in general."
        },
        "SQL_quality": {
            "score": 50, 
            "rationale": "The SQL query is syntactically correct, but it doesn't retrieve the correct data as per the question. It doesn't involve any user data or a measure of 'love' for the movies."
        },
        "consistency": {
            "score": 30, 
            "rationale": "The SQL query doesn't match the intention of the question. The question is about the average number of users who love Stanley Kubrick's movies, but the SQL query is about the average popularity of Stanley Kubrick's movies."
        },
        "significance": {
            "score": 50, 
            "rationale": "The problem is likely to be posed by real users, especially those interested in movie popularity or Stanley Kubrick's movies. The results of the SQL query, however, are not very informative or meaningful in the context of the question."
        }
    }\n"""

    current_date = datetime.date.today().strftime("%Y-%m-%d")

    messages = [
        # {"role": "system", "content": "You are a scorer specializing in SQL and natural language."},
        # {"role": "system", "content": "You are a SQL expert."},
        # 获取当前日期
        {"role": "system", "content": f"You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2023-04 Current date: {current_date}"},
        {"role": "user","content": criteria_prompt},
        {"role": "user","content": question1},
        {"role": "assistant","content": answer1},
        {"role": "user", "content": rate_qa_prompt},
    ]
    print(criteria_prompt+question1+answer1+rate_qa_prompt)
    # exit()
    # try_count = 0
    completion = completion_with_backoff(model=model_choice, messages=messages,temperature=0)
    response = completion.choices[0].message.content
    json_response = extract_json_objects(response)
    if json_response:
        return json_response
    else:
        print(response)
        return {'error':'error decoding JSON response'}

def batch_score_by_gpt4(question_sql_list=[], model_choice="gpt-4-0125-preview"):
    """
    Scores the given question-SQL pair using a language model.

    Args:
        question (str): The question to be scored.
        sql (str): The SQL query to be scored.
        model_choice (str): The choice of language model to use for scoring.

    Returns:
        dict: A dictionary containing the scores for question quality, SQL quality, consistency, and significance.
            The scores are in the range of 0 to 100.

    Example:
        >>> score_by_llm("What is the capital of France?", "SELECT capital FROM countries WHERE name = 'France'")
        {'question_quality': 85, 'SQL_quality': 90, 'consistency': 80, 'significance': 95}
    """


    criteria_prompt = (
        "Based on the following question-SQL pair, rate 'question_quality', 'SQL_quality', 'consistency', and 'significance' "
        "on a scale from 0 to 100. The scores should closely align with the following expectations:\n\n"
        "- 'question_quality' should reflect the clarity and fluency of the question and how relevant it is to potential users.\n"
        "- 'SQL_quality' should reflect the correctness of the SQL query in terms of syntax and its ability to retrieve the correct data as per the question.\n"
        "- 'consistency' should reflect how closely the SQL query matches the intention of the question.\n"
        "- 'significance' should reflect how likely the query is to be posed by real users and how informative and meaningful the results of the SQL query are.\n\n"
    )

    rate_qa_prompt = (
        # "Based on above guidelines, provide the scores for each criterion in a JSON format. Here is the question-SQL pair:\n\n"
        "Below are all the question-SQL pairs that need to be evaluated. Each question-SQL is given in the form of a 2-tuple like (question, SQL) in a list.\n"
        "Please evaluate each question-SQL pair separately and add in response list with no key.\n"
        # "Fill in the rationale field in the json in a short language\n"
        f"{question_sql_list}"
        # "Reference: movie_popularity field means Number of Mubi users who love this movie\n"
        # "Use the information provided to assign scores that align with the specified expectations."
        "Ensure every question-SQL pair is evaluated separately and the response is a list of JSON objects.\n"
        "Give me the reason and insert into json format like the example given above.\n"
        # "Give me the score and reason and insert into json format."
    )

    example_question  = "What is the average number of Mubi users who love movies directed by Stanley Kubrick?"
    example_sql = "SELECT AVG(movie_popularity) FROM movies WHERE director_name = 'Stanley Kubrick'"
    
    question1 = (
        "Based on above guidelines, provide the scores for each criterion in a JSON format. Here is the question-SQL pair:\n\n"
        f"{(example_question, example_sql)}\n"
        # "Use the information provided to assign scores that align with the specified expectations."
        # "Give me the score and reason and insert into json format.\n"
    )
    
    answer1 = """{
        "question_quality": {
            "score": 90, 
            "rationale": "The question is clear and fluent, and it is relevant to potential users, especially those interested in Stanley Kubrick's movies or movie popularity in general."
        },
        "SQL_quality": {
            "score": 50, 
            "rationale": "The SQL query is syntactically correct, but it doesn't retrieve the correct data as per the question. It doesn't involve any user data or a measure of 'love' for the movies."
        },
        "consistency": {
            "score": 30, 
            "rationale": "The SQL query doesn't match the intention of the question. The question is about the average number of users who love Stanley Kubrick's movies, but the SQL query is about the average popularity of Stanley Kubrick's movies."
        },
        "significance": {
            "score": 50, 
            "rationale": "The problem is likely to be posed by real users, especially those interested in movie popularity or Stanley Kubrick's movies. The results of the SQL query, however, are not very informative or meaningful in the context of the question."
        }
    }\n"""
    # exit()
    # print(f'{answer1}')
    # exit()
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    messages = [
        # {"role": "system", "content": "You are a scorer specializing in SQL and natural language."},
        # {"role": "system", "content": "You are a SQL expert."},
        # 获取当前日期
        {"role": "system", "content": f"You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2023-12 Current date: {current_date}"},
        {"role": "user","content": criteria_prompt},
        {"role": "user","content": question1},
        {"role": "assistant","content": answer1},
        {"role": "user", "content": rate_qa_prompt},
    ]
    # print(criteria_prompt+question1+answer1+rate_qa_prompt)
    # exit()
    # try_count = 0
    completion = completion_with_backoff(model=model_choice, messages=messages,temperature=0)
    global total_tokens_used
    global prompt_tokens_used

    global output_tokens_used
    total_tokens_used+=completion.usage.total_tokens
    prompt_tokens_used+=completion.usage.prompt_tokens
    output_tokens_used+=completion.usage.completion_tokens
    print("one batch cost: ", completion.usage.total_tokens)
    response = completion.choices[0].message.content
    
    json_response = extract_json_objects(response)
    if json_response:
        return json_response
    else:
        print(response)
        return {'error':'error decoding JSON response'}

def batch_score_by_llm(input_directory: str, output_directory: str, model_choice="gpt-3.5-turbo"):
    """
    Batch scores the questions and SQL queries in JSON files within the input directory using the specified language model.

    Args:
        input_directory (str): The directory path containing the input JSON files.
        output_directory (str): The directory path where the modified JSON files with scores will be saved.
        model_choice (str, optional): The choice of language model to use for scoring. Defaults to "gpt-3.5-turbo".

    Returns:
        None
    """
    # Function implementation goes here
    start_time = time.time()  # 记录开始时间
    #  Read all JSON files path in the directory
    # 添加处理进度条显示
    json_files_path = []
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)
            json_files_path.append(file_path)

    for file_path in tqdm(json_files_path, desc="Processing json files"):
        filename = os.path.basename(file_path)
        start_time = time.time()  # 记录开始时间
        with open(file_path, "r", encoding="utf-8") as file:
            # print(file_path)
            json_data = json.load(file)
        for qa in tqdm(json_data, desc="Processing QA pairs in "+filename):
            response_score = score_by_llm(question=qa["question"], sql=qa["query"], model_choice=model_choice)
            qa["score"] = response_score
        # Save the modified JSON data as a new file
        # 检查output_directory是否存在，不存在则创建
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        output_file_path = os.path.join(output_directory, filename)
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            tqdm.write('writing to file: '+str(output_file_path))
            json.dump(json_data, output_file, ensure_ascii=False)
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算运行时间
        tqdm.write(f"The file {filename} was processed in {elapsed_time} seconds.")
    
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算运行时间

    print(f"The code ran in {elapsed_time} seconds.")

def extract_query_and_question(directory):
    result = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(os.path.join(directory, filename))
                if isinstance(data, list):  # 如果数据是列表
                    for item in data:
                        if 'query' in item and 'question' in item:
                            # print(item)
                            result.append((item['question'], item['query'],item['db_id']))
                else:  # 如果数据是单个对象
                    if 'query' in data and 'question' in data:
                        result.append((data['question'], data['query'],data['db_id']))
    return result

def get_batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]

def save_json_list(file_path, json_data):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([json_data], f)
    else:
        with open(file_path, "r+") as f:
            existing_data = json.load(f)
            if isinstance(existing_data, list):
                existing_data.append(json_data)
            else:
                existing_data = [existing_data, json_data]
            f.seek(0)
            json.dump(existing_data, f)
            f.truncate()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_directory", help="The directory path where the original QA JSON files store")
    parser.add_argument("--output_directory", help="The directory path where the modified JSON files with scores will be saved.", default="./score_output")
    parser.add_argument("--score_model", help="The batch size for processing the QA pairs.", default="gpt-4-turbo-2024-04-09")
    parser.add_argument("--batch_size", type=int, help="The batch size for processing the QA pairs.", default=10)
    # Add more arguments here if needed
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()
    input_directory = args.input_directory
    output_directory = args.output_directory
    score_model = args.score_model
    batch_size = args.batch_size  # 设置你的batch_size

    qa_pairs_with_db_id = extract_query_and_question(input_directory)

    # 如果output_directory不存在，则创建
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    total_batches = len(qa_pairs_with_db_id) // batch_size
    if len(qa_pairs_with_db_id) % batch_size != 0:
        total_batches += 1
    for batch_qa_with_dbid in tqdm(get_batches(qa_pairs_with_db_id, batch_size), total=total_batches, desc="Processing batches"):
        batch_qa = [(q, a) for q, a, _ in batch_qa_with_dbid]
        batch_score_lst = batch_score_by_gpt4(batch_qa, model_choice=score_model)
        print(batch_score_lst)
        for qa_pair_with_dbid, score in zip(batch_qa_with_dbid, batch_score_lst):
            question, sql, db_id = qa_pair_with_dbid
            json_data = {
                "db_id": db_id,
                "question": question,
                "sql": sql,
                "score": score
            }
            file_name = f"{db_id}.json"
            file_path = os.path.join(output_directory, file_name)
            save_json_list(file_path, json_data)
        # break
    print("total_tokens_used: ",total_tokens_used)
    print("prompt_tokens_used: ",prompt_tokens_used)
    print("output_tokens_used: ",output_tokens_used)