import json
import random
from pathlib import Path
from types import SimpleNamespace
from typing import List, Tuple, Union, Any, Dict
#from tools.training_data_builder.training_data_builder import transform_sample
# from training_data_builder import transform_sample
# from spacy.lang.en import English
import sys
import os

# 将当前工作目录添加到 Python 模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
# 获取父目录路径
parent_dir = os.path.dirname(current_dir)
# 将父目录路径添加到 Python 模块搜索路径
sys.path.append(parent_dir)
# 获取父目录的父目录路径
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from typing import List
# nlp = English()

random.seed(42)


from intermediate_representation.sem2sql.sem2SQL import transform, build_graph
# DO NOT remove this imports! They are use by the dynamic eval() command in to_semql()
from intermediate_representation.semQL import Sup, Sel, Order, Root, Filter, A, Op, N, C, T, V, Root1, Action
from tools.transform_generative_schema import GenerativeSchema
from tools.transform_generative_schema import transform as transform_generative_schema

from synthetic_data.sample_queries.sample_query import sample_query
from synthetic_data.specific_power_types import power_query_types,simple_query_types,complex_query_types
import sys


def get_dev_db_ids(handmade_dev_file: Path) -> list:
    db_id_set = set()
    # 打开JSON文件
    with open(handmade_dev_file, 'r') as file:
        # 解析JSON数据
        data = json.load(file)
        # 遍历每行数据
        for row in data:
            # 提取db_id并添加到集合中
            db_id = row.get('db_id')
            if db_id is not None:
                db_id_set.add(db_id)
    # 将集合转换为列表并返回
    return list(db_id_set)

def get_dev_db_ids_from_dir(db_parent_path: Path) -> list:
    # 获取目录下的所有文件夹名，整理成不重复的列表返回
    return list(set([x.name for x in db_parent_path.iterdir() if x.is_dir()]))
    
def init_generative_schema_spider_dev(handmade_dev_file: Path, original_schema_path: Path, new_schema_parent_path: Path):
    db_ids = get_dev_db_ids(handmade_dev_file)

    for db_id in db_ids:
        new_schema_path = new_schema_parent_path / db_id / 'generative_schema.json'
        if not new_schema_path.parent.exists():
            new_schema_path.parent.mkdir(parents=True, exist_ok=True)
        transform_generative_schema(original_schema_path, new_schema_path, tables_of_interest = [], db_id=db_id)

def init():
    """
    this method is called for init the generative schemata
    """
    # data_path = Path('data/spider')
    # original_schema_path = data_path / 'original' / 'tables.json'
    # new_schema_parent_path = data_path / 'generative'

    data_path = Path('data/world_soccer_db_20210601')
    original_schema_path = data_path / 'tables.json'
    new_schema_parent_path = data_path / 'generative'
    
    init_generative_schema_spider_dev(original_schema_path, original_schema_path, new_schema_parent_path)


def generate_spider_dev_queries(db_parent_path, template_level = 'complex', db_ids = []):
    # data_path = Path('data/spider')
    # original_schema_path = data_path / 'original' / 'tables.json'
    # new_schema_parent_path = data_path / 'generative'
    # db_parent_path = 'C:/Users/86130/Downloads/spider/spider/database'

    # data_path = Path('data/world_soccer_db_20210601')
    # original_schema_path = data_path / 'tables.json'
    # new_schema_parent_path = data_path / 'generative'
    # db_parent_path = r'C:\Users\86130\Downloads\sql\data\world_soccer_db_20210601'

    # _db_ids = get_dev_db_ids(original_schema_path)
    _db_ids = get_dev_db_ids_from_dir(db_parent_path)

    if any(db_ids):
        db_ids = [db_id for db_id in db_ids if db_id in _db_ids]
    else:
        db_ids = _db_ids

    if template_level == 'simple':
        query_types = simple_query_types()
    elif template_level == 'complex':
        query_types = complex_query_types()
    else:
        query_types = power_query_types()



    for db_id in db_ids:
        # db_path = os.path.join(db_parent_path, db_id, f'{db_id}.sqlite')
        
        db_path = os.path.join(db_parent_path, db_id, f'{db_id}.db')
        
        original_schema_path = db_parent_path/ db_id / 'tables.json'
        with open(original_schema_path, 'r') as f_in:
            original_schemata = json.load(f_in)
        new_schema_parent_path = db_parent_path/ db_id /'generative'

        db_config = SimpleNamespace(path=db_path)
        
        if not (db_parent_path / db_id / template_level).exists():
            (db_parent_path / db_id / template_level).mkdir(parents=True, exist_ok=True)
        output_json = db_parent_path / db_id / template_level/'synthetic_queries.json'
        original_schema = [os for os in original_schemata if os['db_id'] == db_id][0]
        generative_schema_path = new_schema_parent_path / 'generative_schema.json'
        generative_schema = GenerativeSchema(generative_schema_path)
        for idx, (query_type, factor) in enumerate(query_types.items()):
            max_success = 5
            succeed = 0
            max_iter = 50
            attemps = 0
            max_success = max_success * factor
            sampled_queries, res = [], []
            while attemps < max_iter and succeed < max_success:
                try:
                    sampled_query, sampled_query_replaced = sample_query(query_type, original_schema, generative_schema, db_config)
                    if sampled_query not in sampled_queries:
                        sampled_queries.append(sampled_query)
                        res.append(
                            {
                            'db_id': db_id,
                            'template_id': idx,
                            'query_type': query_type, 
                            'query': sampled_query,
                            'readable_query': sampled_query_replaced
                        }
                        )
                        succeed += 1
                    else: # counted it as a failed attemp
                        attemps += 1
                except ValueError as e:
                    print(e)
                    attemps += 1
            if output_json.exists():
                with open(output_json, 'r') as f_in:
                    _res = json.load(f_in)
            else:
                _res = []
            _res.extend(res)
            with open(output_json, 'w') as f_out:
                json.dump(_res, f_out, indent=2)
            print(f'{str(len(_res))} results persisted')

        print( f'creating synthetic queries of "{db_id}" successfully')

# def concat_synthetic_queries(output_json_path = None, db_ids = [], max_results = 0):
    
#     # data_path = Path('data/spider')
#     # original_schema_path = data_path / 'original' / 'tables.json'

#     data_path = Path('data/world_soccer_db_20210601')
#     original_schema_path = data_path / 'tables.json'
#     new_schema_parent_path = data_path / 'generative'

#     if output_json_path is None:
#         output_json_path = new_schema_parent_path / 'synthetic_queries.json'
#     with open(original_schema_path, 'r') as f_in:
#         original_schemata = json.load(f_in)
#     res = []
#     _db_ids = get_dev_db_ids(original_schema_path)
#     if any(db_ids):
#         db_ids = [db_id for db_id in db_ids if db_id in _db_ids]
#     else:
#         db_ids = _db_ids
#     for db_id in db_ids:
#         synthetic_queries_file = new_schema_parent_path / db_id / 'synthetic_queries.json'
#         if synthetic_queries_file.exists():
#             with open(synthetic_queries_file, 'r') as f_in:
#                 temp_res = json.load(f_in)
#                 temp_res = check_spider_compabilities(temp_res, original_schemata)
#                 if max_results > 0 and max_results < len(temp_res):
#                     temp_res = sorted(random.sample(temp_res, max_results), key=lambda x: x['template_id'])
#                 res.extend(temp_res)
#     with open(output_json_path, 'w') as f_out:
#         json.dump(res, f_out, indent=2)
#         print(f'successfully generated {str(len(res))} synthetic Spider Dev data under {str(output_json_path)}')


# def check_spider_compabilities(data, original_schemata):
#     samples = []
#     schema_dict = {}
#     for schema in original_schemata:
#         db_id = schema['db_id']
#         schema_dict[db_id] = schema
#     check_failed = 0
#     for sample in data:
#         sample['question'] = "Dummy question for checking sanity."
#         try:
#             transformed = transform_sample(sample, schema_dict, nlp.tokenizer)
#             del sample['question']
#             samples.append(sample)
#         except Exception as e:
#             print(f'Error while transforming sample: {e}')
#             print(f'Sample: {sample}')
#             check_failed += 1
#     print(f'Sanity Check for {str(len(data))} generated samples, found {str(check_failed)} samples with failed check. Finally {str(len(samples))} samples created')
#     return samples
    

def main():
    # init()
    print(get_dev_db_ids_from_dir(Path('data/')))
    if len(sys.argv) > 1:
        template_level = sys.argv[1]
        generate_spider_dev_queries(Path('data/'), template_level)
    else:
        print("Please provide a template level as a command line argument.")
    # generate_spider_dev_queries(db_ids=['college_2'])
    # generate_spider_dev_queries()
    # concat_synthetic_queries(max_results = 200) # set max_results to 0 to have all results

if __name__ == '__main__':
    main() 