# Train Set Overview

This repository contains a dataset for training text-to-SQL models. The dataset includes single-turn text-to-SQL data, as well as database creation information.

## File Structure

- **train_databases_create_info/**
  - Contains SQL DDL files used to create the training databases.
- **train.json**
  - Contains single-turn text-to-SQL dialogue data.

## train.json

This file contains single-turn questions and their corresponding SQL queries, along with metadata about the quality of the questions and queries. The structure is as follows:

```json
{
    "DatabaseName": [
        {
            "db_id": "DatabaseName",
            "question": "NL question",
            "sql": "Gold SQL query",
            "score": {
                "question_quality": {
                    "score": 0-100,
                    "rationale": "Rationale for question quality score"
                },
                "SQL_quality": {
                    "score": 0-100,
                    "rationale": "Rationale for SQL quality score"
                },
                "consistency": {
                    "score": 0-100,
                    "rationale": "Rationale for consistency score"
                },
                "significance": {
                    "score": 0-100,
                    "rationale": "Rationale for significance score"
                }
            },
            "result": "Whether the SQL query has results"
        },
        ...
    ],
    ...
}
```

### Example Entry

```json
{
    "Accidents": [
        {
            "db_id": "Accidents",
            "question": "What is the average breathalyzer test result for each accident scene?",
            "sql": "SELECT avg( T1.alkotest), T2.opis_prizorisce FROM oseba AS T1 JOIN nesreca AS T2 ON T1.id_nesreca = T2.id_nesreca GROUP BY T2.opis_prizorisce",
            "score": {
                "question_quality": {
                    "score": 85,
                    "rationale": "The question is clear, asking for average breathalyzer results by accident scene."
                },
                "SQL_quality": {
                    "score": 90,
                    "rationale": "The SQL query correctly computes the average breathalyzer test result for each accident scene."
                },
                "consistency": {
                    "score": 95,
                    "rationale": "The SQL query matches the intention of the question very closely."
                },
                "significance": {
                    "score": 80,
                    "rationale": "The query is significant for analyses related to accident scenes and driving under the influence."
                }
            },
            "result": "Yes"
        }
    ]
}
```

## Usage

Use this dataset to train text-to-SQL models.

## License

This project is licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/ "Licensed under Creative Commons Attribution 4.0 International") - see the LICENSE file for details.
