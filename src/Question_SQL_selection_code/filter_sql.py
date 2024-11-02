import argparse
import json
import os

def read_json_files(folder_path):
    json_objects = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                json_objects.extend(json_data)
    return json_objects

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read JSON files in a folder')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing JSON files')
    parser.add_argument('output_folder', type=str, help='Path to the output file')
    
    args = parser.parse_args()

    # 如果output_folder不存在，创建文件夹
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    score_threshold = 75
        
    input_folder_path = args.input_folder
    for file_name in os.listdir(input_folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_folder_path, file_name)
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                output_json_data = []
                for item in json_data:
                    score = item['score']
                    if isinstance(score, dict):
                        if isinstance(score['question_quality'], dict):
                            question_quality_score = score['question_quality']['score']
                            SQL_quality_score = score['SQL_quality']['score']
                            consistency_score = score['consistency']['score']
                            significance_score = score['significance']['score']
                            if question_quality_score >= score_threshold and SQL_quality_score >= score_threshold and consistency_score >= score_threshold and significance_score >= score_threshold:
                                output_json_data.append(item)
                        elif isinstance(score['question_quality'], int or float):
                            question_quality_score = score['question_quality']
                            SQL_quality_score = score['SQL_quality']
                            consistency_score = score['consistency']
                            significance_score = score['significance']
                            if question_quality_score >= score_threshold and SQL_quality_score >= score_threshold and consistency_score >= score_threshold and significance_score >= score_threshold:
                                output_json_data.append(item)
                        else:
                            pass
                output_file_path = os.path.join(args.output_folder, file_name)
                with open(output_file_path, 'w') as output_file:
                    json.dump(output_json_data, output_file, indent=4)