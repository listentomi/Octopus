#### Project Overview

This project consists of two Python scripts, `filter_sql.py` and `score.py`, used to extract question-SQL pairs from an input directory and score these pairs using OpenAI's GPT-4 model.

#### File Descriptions

1. `filter_sql.py`
   
   - Function: Extracts SQL queries and questions with database IDs from the specified directory and saves them as JSON files.
   - Key Functions:
     - `extract_query_and_question(input_directory)`: Extracts question and SQL pairs from the specified directory.
     - `save_json_list(file_path, json_data)`: Saves JSON data to the specified file path.
     - `get_batches(data, batch_size)`: Divides the data into batches of the specified size.

2. `score.py`
   
   - Function: Scores the question-SQL pairs using the GPT-4 model and saves the results to JSON files.
   - Key Functions:
     - `batch_score_by_gpt4(qa_pairs, model_choice="gpt-4")`: Batch scoring function.
     - `test_score_by_gpt4(question="question", sql="sql", model_choice="gpt-4")`: Tests the scoring of a single question-SQL pair.
     - `parse_arguments()`: Parses command line arguments.

#### Installation and Usage

1. Install dependencies:
   
   `pip install openai tqdm`

2. Run `score.py`:
   
   sh
   
   复制代码
   
   `python score.py <input_directory> --output_directory <output_directory> --score_model <model_choice> --batch_size <batch_size>`
   
   Example:
   
   `python score.py ./input --output_directory ./score_output --score_model gpt-4 --batch_size 10`

3. Run `filter_sql.py`:
   
   `python filter_sql.py <input_directory> --output_directory <output_directory>`

#### Notes

- The input directory for `filter_sql.py` should contain JSON files with `question`, `sql`, and `db_id` fields.
- `score.py` uses OpenAI's GPT-4 model for scoring, so ensure that the OpenAI API key is configured.
- If a RateLimitError occurs, the script will wait for a while before retrying.