import argparse
import time
import json
from openai import APIConnectionError, OpenAI
from progress.bar import Bar
import concurrent.futures
import re
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where
import sqlparse.tokens as Token
import mysql.connector
from src.qa import makecomversation
import os
import pandas as pd

remove_aliases_input = 0
remove_aliases_output = 0

place_tablename_input = 0
place_tablename_output = 0

rough_tranlate_clause_input = 0
rough_tranlate_clause_output = 0

fewshot_tranlate_clause_input = 0
fewshot_tranlate_clause_output = 0

the_final_translate_input = 0
the_final_translate_output = 0

en2ch_input = 0
en2ch_output = 0

# 取消别名 300 token
def remove_aliases(sqls):

    prompt = """You are a SQL parsing expert. You need to remove the aliases in sql statement, then return the SQL statement without the aliases. Here is one examples:
    WITH clause is not considered in this task.
    before:
          "SELECT DISTINCT count(anon_1.c_4200) OVER (PARTITION BY anon_1.description) AS c_4528, 
          anon_1.c_141, 
          anon_1.description 
          FROM (
            SELECT film_text.description AS description, 
            count(distinct(film_text.film_id)) AS c_141, 
            count(film_text.title) OVER (ORDER BY film_text.title) AS c_4200 
            FROM film_text 
            WHERE (film_text.film_id >= %(film_id_1)s) 
            GROUP BY film_text.title, film_text.description, film_text.film_id) AS anon_1
    after: 
          SELECT DISTINCT COUNT(film_text.title) OVER (PARTITION BY film_text.description), 
                COUNT(DISTINCT film_text.film_id) 
                film_text.description
          FROM (
              SELECT film_text.description, 
                    COUNT(DISTINCT film_text.film_id) , 
                    COUNT(film_text.title) OVER (ORDER BY film_text.title)
              FROM film_text
              WHERE film_text.film_id >= %(film_id_1)s
              GROUP BY film_text.title, film_text.description, film_text.film_id
          ) ;
    """

    usercontent = f""" You need to remove the aliases from the SQL provided below, then return the SQL statement without the aliases.
    Make sure you return a valid SQL statement, do not generate any other content, it you find problem in sql provided, ignore it.  

    The SQL statements are: 
    {sqls}
    """

    return_format = '[{"sql":"SQL statement without the aliases"},{"sql":"SQL statement without the aliases"}]'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global remove_aliases_input
    global remove_aliases_output
    remove_aliases_input += input_tokens
    remove_aliases_output += ouput_tokens

    return result['sql'], input_tokens, ouput_tokens


# 添加表名 200token
def place_tablename(sql):
    prompt = """You are a SQL parsing expert. You need to add the table name to all the indicator that appear in the sql statement. """

    usercontent = f""" 
        You need to add the table name to all the indicator that appear in the sql statement。
        Make sure there are no omissions. 
        Do not abbreviate the table name. 
        if the table is is already correctly formatted return the original SQL statement.

        The SQL statement is: 
        {sql}
        """
    
    return_format = '{"sql":"SQL statement with the table name added to all the indicator"}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global place_tablename_input
    global place_tablename_output
    place_tablename_input += input_tokens
    place_tablename_output += ouput_tokens

    return result['sql'], input_tokens, ouput_tokens

# 替换运算符
def replace_logical_operators(sql):
    WHERE_OPS = ('not', 'between', '=', '>', '<', '>=', '<=', '!=', 'in', 'like', 'is', 'exists')
    WHERE_OPS_NL = ('not', 'between', 'equal to', 'more than', 'less than', 'no less than', 'no more than', 'not equal to', 'in', 'like', 'is', 'exists')


    for op, nl in zip(WHERE_OPS, WHERE_OPS_NL):
                            op_str = f" {op} "
                            if  op_str in sql:
                                sql = sql.replace(op_str, f" {nl} ")
                            
    return sql

#### 预处理：

def preprocess(sql, jump=True):
    if not jump:    
        sql, inputs1, outputs1 = remove_aliases(sql)  
        sql, inputs2, outputs2 = place_tablename(sql)
    sql = replace_logical_operators(sql)
    return sql, inputs1, inputs2, outputs1, outputs2


def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is Token.DML and item.value.upper() == 'SELECT':
            return True
    return False


class SQLNode:
    def __init__(self, node_type, value=None, sub_list=None):
        self.type = node_type
        self.value = value
        self.sub_list = sub_list or []

    def __repr__(self):
        return f"node(tt={self.type}, vv={self.value}, ss={self.sub_list})"
    

    def has_sublist(self):
        return len(self.sub_list) > 0
    
    def get_clause(self, depth):
        return str(str(depth)+' '+self.type+' '+self.value)
    
    def merge_subsql(self, depth=1):
        clause_list = []
        for node in self.sub_list:
            if node.has_sublist(): # 有下级管理下级
                clause_list += node.merge_subsql(depth+1)
            
            # 此时node有子节点，而子节点没有子节点，即只有一层嵌套的情况
            clause_list += node.merge_select(depth)
            clause_list += node.merge_from(depth)
            clause_list += node.merge_where(depth)
            # 没有下级则等待管理


            if depth == 1: # 最高级管理，1级没有上级，在这里处理
                clause_list.append(node.get_clause(depth))
        return clause_list
    
    # 下面的merge方法只考虑有一层嵌套的情况：

    def merge_select(self, depth):
        clause_list = []
        if ('SELECT' in self.type ) and (len(self.sub_list) > 0):
            clause_list = [subnode.get_clause(depth) for subnode in self.sub_list]
        return clause_list
        

    def merge_from(self, depth):
        clause_list = []
        if ('FROM' in self.type) and (len(self.sub_list) > 0):
            clause_list = [subnode.get_clause(depth+1) for subnode in self.sub_list if not any(item in subnode.type for item in ['SELECT', 'FROM', 'ORDER BY'])]
            self.sub_list = []
        return clause_list
                    

    def merge_where(self, depth):
        clause_list = []
        if ('WHERE' in self.type) and (len(self.sub_list) > 0):
            # 把subselect1, subselect2替换成相应select的内容
            mapping_table = {
            }
            for item in self.sub_list:
                if 'SELECT' in item.type:
                    mapping_table[item.type] = item.value
                    # remove item from sub_list
                    self.sub_list.remove(item)
                    
            # 替换函数
            def replace_subselect(match):
                subselect_key = match.group(0)  # 获取整个匹配的子字符串，例如：subselect1
                subselect_number = match.group(1)  # 获取匹配的数字部分，例如：1
                mapping_key = f'SELECT{subselect_number}'
                return mapping_table.get(mapping_key)

            # 正则表达式匹配subselect后的数字
            pattern = re.compile(r'subselect(\d+)')

            # 使用sub()函数进行替换
            self.value = pattern.sub(replace_subselect, self.value)

            # self.value =  self.value + ' ' + self.sub_list[0].value
            # self.sub_list.pop(0)

            clause_list = [subnode.get_clause(depth+1) for subnode in self.sub_list]
            self.sub_list = []
        return clause_list


## 子句粗分解    
def decompose(sql):
    parsed = sqlparse.parse(sql)
    stmt = parsed[0]

    # 粗分解
    result,_,_ = split_by_keywords(stmt)
    return result


def split_by_keywords(tokenlist, subselect_num = 0): # subselect_num子查询数量
    # 每一递归处理同一层的token
    # 同一层内可能包含并行嵌套，例如SELECT a, (SELECT b FROM c), (SELECT e FROM f) FROM d，因此需要对subselect编号

    KEYWORDS = {'SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT', 'WITH', 'UNION', 'INTERSECT', 'EXCEPT'}
    
    keyword=None # 本层的关键字，当本层不是有效sql层时，keyword始终为None
    clauses='' # 本层的关键字后面的子句
    subsqllist=[] # 本层的子查询
    nodelist = [] # 本层的节点集合

    for token in tokenlist:
        # 为什么采用尾递归的形式：
        # 1. 因为一个token 首先是一个group，其次才会是一个子查询。我们重点考虑的是子查询嵌套的情况

        if is_subselect(token):  
            # 当前的token 是一个子查询，下面的部分需要提取该子查询的Node集合
            s1 = token
            subselect_num += 1
            subsql, _, _ = split_by_keywords(s1.tokens, subselect_num)  
            # 对于同一层的子查询， 不需要区分，所以可以全部归纳到subsqllist中：
            subsqllist += subsql 
            clauses += 'subselect'+str(subselect_num) # 用subselect代替子查询的内容
      
        elif isinstance(token, Where):
            # 因为sqlsparse的实现，WHERE相比其他关键字需要特别处理
            # 这时候的token是一整个where语句

            # 返回的subsql事实上是一个只包含where节点的列表
            subsql, res_clause, _ = split_by_keywords(token.tokens, subselect_num)
            where_node = subsql[0]
            nodelist.append(where_node)

        elif token.value.upper() in KEYWORDS:
            # 当前的Token 是一个关键字
            # 除了第一次遇见关键字即第一个SELECT之外，或者With，其他时刻都不可能是None
            # 第一次遇见关键字，不需要创建新的节点
            if keyword is not None: 
                
                nodelist.append(SQLNode(keyword, clauses, subsqllist))
                # 添加完节点后，初始化子查询列表和子句内容   
                clauses = ''
                subsqllist = []

            # 遇到关键字总要更新关键字
            keyword = token.value.upper()+str(subselect_num)

        elif not token.is_group:
            # 当前的token是一个词
            clauses += token.value

        else : 
            # token是一个group(token组)，它可能包含子查询(subsql)，以及其他词（res_clause）
            subsql, res_clause, _ = split_by_keywords(token.tokens, subselect_num)
            subsqllist += subsql
            clauses += res_clause


    if keyword is not None: # 处理最后一个关键字，如果keyword is None说明本层不是一个有效sql层，可能只有两个indentifier，例如a,b
        nodelist.append(SQLNode(keyword, clauses, subsqllist))
        clauses = ''
        subsqllist = []
    
    # 如果该层是有效sql层（keyword is not None）：
        # 一定会有一个nodelist，而subsqllist为空
    # 如果该层不是有效层，例如只有两个indentifier，那么nodelist为空，而subsqllist不为空

    return nodelist+subsqllist, clauses, subselect_num


## 语义合并
def get_clause(sql):
    root_node = SQLNode('ROOT', None, decompose(sql))
    clause_list = root_node.merge_subsql()
    return clause_list


# ，删除所有from
def remove_from(clause_list):
    processed_clauses = []
    for clause in clause_list:
        if 'FROM' not in clause:
            processed_clauses.append(clause)
    return processed_clauses

# 删除所有换行符
def remove_linefeed(clause_list):
    return [clause.replace('\n', '') for clause in clause_list]

# 按照数字排序
def sort_caluse(clause_list):
    def custom_sort(query):
        return int(query.split()[0])
    return  sorted(clause_list, key=custom_sort)

# (搁置) 提取所有的标识符
def extract_identifiers(clause_list):
    for clause in clause_list:
        matches = re.findall(r'\b\w+\.\w+\b', clause)
        matches = list(set(matches))  
    return  matches


def remove_with(clause_list):
    processed_clauses = []
    for clause in clause_list:
        if 'WITH' not in clause:
            processed_clauses.append(clause)
    return processed_clauses


def merge_having(clause_list):
    processed_clauses = []
    havings = []
    for clause in reversed(clause_list):
        if 'HAVING' in clause:
            havings.append(clause)
        elif 'GROUP BY' in clause:
            # 如果有GROUP BY，那么HAVING一定在GROUP BY之前
            if len(havings) > 0:
                by = (clause.split()[2])
                index_by = re.findall(r'[a-zA-Z]+(\d+)', by)[0]
                for having in havings:
                    index_having = re.findall(r'[a-zA-Z]+(\d+)', having.split()[1])[0]
                    if index_having == index_by:
                        processed_clauses.append(clause + clean_clause(having))
                        havings.remove(having)
            else:     
                processed_clauses.append(clause)
        else:
            processed_clauses.append(clause)
    return list(reversed(processed_clauses))


def clean_clause(clause):
    cleaned_clause = re.sub(r'^\d+\s*([\w\s]+?)\d+', r'\1', clause)
    return cleaned_clause.strip()


def clean_clause_list(clause_list):
    return [clean_clause(clause) for clause in clause_list]


# 后处理：
def after_process(clause_list):
    clause_list = remove_from(clause_list)
    clause_list = remove_linefeed(clause_list)
    clause_list = sort_caluse(clause_list)
    clause_list = remove_with(clause_list)
    clause_list = merge_having(clause_list)
    clause_list = clean_clause_list(clause_list)
    return clause_list


# 提取sql相关字段
def get_indicators(clause_list):
  pattern = r'\b\w+\.\w+\b'
  sql_indicators = []
  for clause in clause_list:
    matches = re.findall(pattern, clause)
    sql_indicators += matches
  return sql_indicators # [table.column, table.column, ...]


# 获取字段描述
def get_sql_descriptions(cluse_list, db_name = None):
    if db_name is None:
        return None
    
    des_path = f'./database_descriptions/{db_name}_descriptions.csv'

    if not os.path.exists(des_path):
        return None
    
    descriptions = pd.read_csv(des_path)


    indicators = get_indicators(cluse_list)

    relevent_descriptions = []
    for indicator in indicators:
        table, column = indicator.split('.')
        try:
            # print()
            descirption = descriptions[(descriptions['table'] == table) & (descriptions['column'] == column)]['description'].values[0]
            relevent_descriptions.append(f'column {column} in table {table} is {descirption}. ')
        except KeyError:
            pass

    return relevent_descriptions
        

# 粗翻译,翻译到接近自然语言,没有特殊标记符号,和类似函数的表达形式.  200 tokens
def rough_tranlate_clause(sentence):
    prompt = """You are a Translator."""

    usercontent = f""" 
    Translate the sentence provided into spoken English, not contain any special symbols except commas and periods.
    Only returns the translated sentence, do not generate any other content, such as "The caluse is: ...".
    if you have trouble doing it or hold that nothing need to be changed, just return the original sentence,
    the returned sentence is either the Translated sentence or the original sentence, but we encourage you to translate the sentence even if the changes are minor.
    The sentence is: 
    {sentence}
    """

    return_format = '{"sentence":"translated sentence"}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global rough_tranlate_clause_input
    global rough_tranlate_clause_output
    rough_tranlate_clause_input += input_tokens
    rough_tranlate_clause_output += ouput_tokens

    return result['sentence'], input_tokens, ouput_tokens


def rough_tranlate(clause_list):
    answer = []
    input_tokens = 0
    output_tokens = 0
    for clause in clause_list:
        sentence, inputs, outputs = rough_tranlate_clause(clause)
        input_tokens += inputs
        output_tokens += outputs
        answer.append(sentence)
    return answer, input_tokens, output_tokens

# 精翻译，few shot Translation，作为问题生成的提示  500 tokens
def fewshot_tranlate_clause(clause):
    
    clause_type = clause.split()[0].lower()
    examples = get_examples(clause_type, 10)

    example_prompt = "Here is some examples:" if len(examples)>0 else ""
    examples = "" if len(examples) == 0 else examples
    prompt = f"""You are a language expert. You need to translate the sql clause provided and then return the colloquial result. 
    {example_prompt}
    {examples}
    """

    usercontent = f""" You need to translate the sql clause provided and then return the colloquial result. 
    Do not generate any other content, such as "The paragraph means: ", just the result. 
    if you can't translate the sql clause, return the clause provided, don't reply content as such"'The SQL clause is not valid. Please provide a valid SQL clause.'".
    The sql clause is: 
    {clause}
    """

    return_format = '{"colloquialized":"colloquialized result"}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global fewshot_tranlate_clause_input
    global fewshot_tranlate_clause_output
    fewshot_tranlate_clause_input += input_tokens
    fewshot_tranlate_clause_output += ouput_tokens
    return result['colloquialized'], input_tokens, ouput_tokens

import random
def get_examples(type, num):
    with open('Translation_examples.txt', 'r') as f:
        Translation_examples = f.readlines()
    examples = []
    if type == 'select':
        select_examples = list(set([line for line in Translation_examples if line.startswith('select')] ))
        random_selection = random.sample(select_examples, num)
    elif type == 'where':
        where_examples = list(set([line for line in Translation_examples if line.startswith('where')] ))
        random_selection = random.sample(where_examples, num)
    elif type == 'order':
        order_examples = list(set([line for line in Translation_examples if line.startswith('order')] ))
        random_selection = random.sample(order_examples, num)
    elif type == 'group':
        order_examples = list(set([line for line in Translation_examples if line.startswith('group')] ))
        random_selection = random.sample(order_examples, 5)
    else: 
        return []
    

    for line in random_selection:
        parts = line.split('|')
        examples.append({'before': parts[0].strip(), 'colloquialized': parts[1].strip()})
    return examples


def get_hint(simplified_sql):
    sub_questions = []
    input_tokens = 0
    output_tokens = 0
    for sentence in simplified_sql:
        sub_question, inputs, outputs = fewshot_tranlate_clause(sentence)
        sub_questions.append(sub_question)
        input_tokens += inputs
        output_tokens += outputs
    return sub_questions, input_tokens, output_tokens


# 最终翻译  500 tokens
def the_final_translate(original_sql, simplified_version, hints, descriptions):
    with open('spider_examples.txt', 'r', encoding='utf-8') as f:
        spider_examples = f.readlines()
    random_selection = random.sample(spider_examples, 10)

    is_descriptions = descriptions is not None and len(descriptions) > 0
    
    prompt = f"""You are a sql to question translation expert. You need to translate the sql provided and then return the coresponding question easy to understand. 
    Especially, when "count(stuff_id)" or "group by stuff_id", we means "how many stuff are there", or "for each stuff", not how many ids are there, don't mention id or IDS if not necessary. 
    and don't use the word "count" or orther function name in the question, say what they do.
    Also, don't mention the table name or column name in the question, or use the word "table" or "column" in the question, guess the realistic meaning from the table name, 
    such as table "address.address" is just a address, the "address.last_update" is just the last update time.
    don't use from clause in the question, and don't use the word "from" in the question, people who ask the question don't need to know where the data is stored.
    most sql i provided contains meaningless parts, if possible, try to ignore those meaningless part in the question.
    here is some examples:
    {random_selection}
    """

    usercontent = f""" You need to translate the sql provided and then return coresponding question. 
    Because sometimes SQL is too complex to understand, or even contains errors, we will also provide a simplified version(a clause list, contains main information about the sql) for reference. 
    In addition, we will also provide some tips to introduce the meaning of this sql, and what the generated question is mostly about.
    Do not generate any other content, such as "The question is: ", just the question of the sql itself. 
    if you can't translate the sql, return the simplified version provided(needs to be concat in right order), don't reply content as such "The SQL clause is not valid. Please provide a valid SQL clause.".
    """ 
    if is_descriptions:
        temp = f"""
        We will provide the descriptions of the columns in SQL, which you can take as reference.
        """
        usercontent += temp
    

    usercontent +=f"""
    The original sql is: 
    {original_sql}
    The simplified version is:
    {simplified_version}
    The hints are:
    {hints}
    """
    if is_descriptions:
        usercontent += f"""
        The descriptions of the columns are:
        {descriptions}
        """

    return_format = '{"question":" coresponding question to the sql provided"}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global the_final_translate_input
    global the_final_translate_output
    the_final_translate_input += input_tokens
    the_final_translate_output += ouput_tokens
    return result['question'], input_tokens, ouput_tokens


def getfileinfo_from_path(path):
    # 获取文件名
    file_name = os.path.basename(path)

    # 获取文件类型
    file_name, file_type = file_name.split('.')
    return file_name, file_type

# random fewshot 翻译 300tokens
def getAnswer(en):

    with open('./CSpider/en2ch_examples.json', 'r', encoding='utf-8') as f:
        spider_examples = json.load(f)
    random_selection = random.sample(spider_examples, 10)

    examples = ''
    index = 1
    for item in random_selection:
        example = f"examples{index}: \"{item['english question']}\", its Chinese translation is \"{item['chinese question']}\".\n"
        examples += example
        index += 1

    prompt = f"""You are a translation expert. You need to translated the english question to chinese question. 
    当你看到单词unique例如'unique ticket numbers'，它通常是"不同的"意思， 例如
    "for each unique aircraft code" 可以翻译为"每个不同的飞机代码" 而不是"每个独特的飞机代码"。
    here are some examples:
    {examples}
    """

    usercontent = f""" Translate the chinese question provided below, then return the translated english question.
    The english question is: {en} 
    """

    return_format = '{"chinese result":"the chinese translation of provided english question"}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global en2ch_input
    global en2ch_output
    en2ch_input += input_tokens
    en2ch_output += ouput_tokens

    return result['chinese result'], input_tokens, ouput_tokens

# 翻译主函数
def en2ch(en):
    ch, input_tokens, output_tokens = getAnswer(en)
    with open('token_count.txt', 'a') as f:
        f.write(f"en2ch: {en2ch_input} {en2ch_output}\n")
    print("en2ch:",en2ch_input, en2ch_output)
    return ch, input_tokens, output_tokens

# 集合上面方法
def sql2question(sql, db_name = None):
    # 预处理
    clause,inputs1, inputs2, outputs1, outputs2 = preprocess(sql)
    clause_list = get_clause(clause)
    decomposed_clause = after_process(clause_list)

    # 知识生成
    try: 
        descriptions = get_sql_descriptions(decomposed_clause, db_name)
    except Exception as e:
        print("can't get descriptions:", e)
        descriptions = 'no descriptions available, you have to guess from the table name.'
    simplified_sql, inputs3, outputs3 = rough_tranlate(decomposed_clause)
    hint,inputs4, outputs4 = get_hint(simplified_sql)
    
    # 翻译
    question,inputs5, outputs5 = the_final_translate(sql, simplified_sql, hint, descriptions)
    
    # 将token统计数目保存到本地文件
    with open('token_count.txt', 'a') as f:
        f.write(f"remove_aliases: {remove_aliases_input} {remove_aliases_output}\n")
        f.write(f"place_tablename: {place_tablename_input} {place_tablename_output}\n")
        f.write(f"rough_tranlate_clause: {rough_tranlate_clause_input} {rough_tranlate_clause_output}\n")
        f.write(f"fewshot_tranlate_clause: {fewshot_tranlate_clause_input} {fewshot_tranlate_clause_output}\n")
        f.write(f"the_final_translate: {the_final_translate_input} {the_final_translate_output}\n")
    print("remove_aliases:",remove_aliases_input, remove_aliases_output)
    print("place_tablename:",place_tablename_input, place_tablename_output)
    print("rough_tranlate_clause:",rough_tranlate_clause_input, rough_tranlate_clause_output)
    print("fewshot_tranlate_clause:",fewshot_tranlate_clause_input, fewshot_tranlate_clause_output)
    print("the_final_translate:",the_final_translate_input, the_final_translate_output)

    inputs = [inputs1, inputs2, inputs3, inputs4, inputs5]
    outputs = [outputs1, outputs2, outputs3, outputs4, outputs5]
    return question, inputs, outputs
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='SQL to question translation')

    # random seed
    parser.add_argument('--sql_path', type=str, default='salika_sqls.txt', help='输入文件')
    parser.add_argument('--output_path', type=str, default='new_salika.txt', help='结果输出文件')
    parser.add_argument('--json_sql_indicator', type=str, default='sql', help='json文件的保存sql语句的key')
    parser.add_argument('--database', type=str, default='salika', help='数据库名称')

    args = parser.parse_args()

    sql_path = args.sql_path
    output_path = args.output_path
    sql_indicator = args.json_sql_indicator
    print(sql_path, output_path)
    start_time = time.time()

    
    filename, filetype = getfileinfo_from_path(sql_path)

    # 读文件
    with open(sql_path, 'r') as file:
        if filetype == 'json':
            jsonfile = json.load(file)
            original_sqls = []
            for item in jsonfile:
                original_sqls.append(item[sql_indicator])
        else:
            original_sqls = file.readlines()
    

    total_number  = len(original_sqls)
    
    print("read sqls successfully!, total number of sqls: ", total_number, "\n\n")


    bar = Bar(f'{sql_path}:', max=total_number)
    sql_question_pairs = []
    err_list = []
    sql2en_token_count = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_sentence = {executor.submit(sql2question, [sql, filename]): sql for sql in original_sqls}
        
        for future in concurrent.futures.as_completed(future_to_sentence):
            original_sql = future_to_sentence[future]
            
            bar.next()
            try:
                question, input_token_list, output_token_list = future.result()
                sql_question_pairs.append({'sql': original_sql, 'question': question})
                sql2en_token_count.append({'sql':original_sql,"input":input_token_list,"output":output_token_list})
            except Exception as e:
                print("While translate sql sentence:",original_sql,", an errir occurred:", e)
                err_list.append(original_sql)
    
    end_time = time.time()  
    total_time = end_time - start_time
    print(f"\n\ngenerate question for {sql_path} over, {len(err_list)} filed, total time cost {total_time} seconds\n\n")

    english_question = [pair['question'] for pair in sql_question_pairs]
    total_number  = len(english_question)
    bar = Bar(f'{sql_path}:', max=total_number)
    err_list = []
    en_ch_pairs = []

    start_time = time.time()
    en2ch_token_count = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_sentence = {executor.submit(en2ch, en): en for en in english_question}
        
        for future in concurrent.futures.as_completed(future_to_sentence):
            en = future_to_sentence[future]
            bar.next()
            try:
                ch, inputs, outputs = future.result()
                en_ch_pairs.append({'en': en, 'ch': ch})
                en2ch_token_count.append({'en':en,"input":inputs,"output":outputs})
            except Exception as e:
                print("翻译句子",en,"时出现异常:", e)
                err_list.append(en)

    end_time = time.time()  
    total_time = end_time - start_time
    print(f"generate question for {sql_path} finishied. {len(err_list)} total time cost {total_time} seconds\n\n")

    with open('token_count.txt', 'a') as f:
        f.write(f"{sql_path}, {output_path} \n\n")

    with open('token_count.json', 'a') as f:
        f.write(json.dumps({"sql2en":sql2en_token_count, "en2ch":en2ch_token_count}, indent=4, ensure_ascii=False))
        f.write('\n\n')

    # merge
    for item in sql_question_pairs:
        for en_ch_pair in en_ch_pairs:
            if item['question'] == en_ch_pair['en']:
                item['ch'] = en_ch_pair['ch']
                break
    
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 写文件
    with open(output_path, 'w', encoding="utf-8") as file:
        if filetype == 'json':
            jsonresults = []
            # 找到json item的sql和sql_question_pairs的sql对应
            for item in jsonfile: # 为每一个json item找到对应的问题，并添加问题
                for pair in sql_question_pairs:
                    if pair['sql'] == item[sql_indicator]:
                        item['question'] = pair['question']
                        item['chinese question'] = pair['ch']
                        jsonresults.append(item)
                        break # 跳出
            json.dump(jsonresults, file, indent=4, ensure_ascii=False)
        else:
            for item in sql_question_pairs:
                file.write(f"{item['sql']}\n{item['question']}\n{item['ch']}\n\n")
    print(f"file write to {output_path}\n\n")