import os
import json

def merge_json_files(json_files):
    merged_data = []
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                merged_data.extend(data)
            else:
                merged_data.append(data)
    return merged_data

def save_merged_json(merged_data, output_path):
    with open(output_path, 'w') as f:
        json.dump(merged_data, f, indent=4)

def main():
    root_dir = './data'  # Update the path if necessary
    output_path = './merged'  # Update the path if necessary
    os.makedirs(output_path, exist_ok=True)
    for subdir, _, files in os.walk(root_dir):
        if 'simple' in subdir or 'complex' in subdir:
            json_files = [os.path.join(subdir, f) for f in files if f == 'synthetic_queries.json']
            if json_files:
                merged_data = merge_json_files(json_files)
                parent_dir_name = os.path.basename(os.path.dirname(subdir))
                output_file = os.path.join(output_path, f'{parent_dir_name}.json')
                save_merged_json(merged_data, output_file)
                print(f'Merged JSON saved to: {output_file}')

if __name__ == '__main__':
    main()
