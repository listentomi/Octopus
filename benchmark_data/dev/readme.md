# Dev Set Overview

This repository contains datasets for developing and evaluating text-to-SQL models. The datasets include single-turn dialogue data and database creation information for the development phase.

## File Structure

- **dev_databases_create_info/**
  - Contains SQL DDL files used to create the development databases.
- **dev.json**
  - Contains single-turn text-to-SQL dialogue data for the development phase.

## dev.json

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
        }
    ]
}
```

### Example Entry

```json
{
    "AdventureWorks2014": [
        {
            "db_id": "AdventureWorks2014",
            "question": "What are the last modified dates of sales reasons that have not been used in any sales order headers?",
            "sql": "SELECT T1.ModifiedDate FROM SalesReason AS T1 WHERE T1.SalesReasonID NOT IN (SELECT T22.SalesReasonID FROM SalesOrderHeaderSalesReason AS T22)",
            "score": {
                "question_quality": {
                    "score": 85,
                    "rationale": "The question is clear and relevant, asking for specific data related to unused sales reasons."
                },
                "SQL_quality": {
                    "score": 90,
                    "rationale": "The SQL query correctly identifies sales reasons not used in any sales order headers."
                },
                "consistency": {
                    "score": 95,
                    "rationale": "The SQL query matches the intention of the question very closely."
                },
                "significance": {
                    "score": 80,
                    "rationale": "The query is likely to be significant for users analyzing sales data, though it might be somewhat niche."
                }
            },
            "result": "Yes"
        }
    ]
}
```

## Usage

Use these datasets to develop and evaluate text-to-SQL models. The dev set helps refine models and ensure they can handle a variety of single-turn questions accurately.

## License

This project is licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/ "Licensed under Creative Commons Attribution 4.0 International") - see the LICENSE file for details.
