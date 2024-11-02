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
# import mysql.connector
# from src.qa import makecomversation
import os
import pandas as pd


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
    # print(stmt)

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


if __name__=='__main__':
    sql = 'SELECT T1.status FROM loan AS T1 WHERE T1.payments = (SELECT max( T22.payments) FROM loan AS T22 JOIN account AS T23 ON T22.account_id = T23.account_id)'
    clause_list = get_clause(sql)
    decomposed_clause = after_process(clause_list)
    print(decomposed_clause)