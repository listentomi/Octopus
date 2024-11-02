# Generate SQLs on New Sqlite Databases
## requirements
spacy
## preprocess
1. Handle database file suffixes
For sqlite databases, put the database files (.sqlite) into a directory then run `.\preprocess\prepare_sqlite_dbs.py` script
```
 python .\preprocess\prepare_sqlite_dbs.py <db_source_dir> <db_target_dir> 
```
2. Extract information from databases
run `.\preprocess\get_info_sqlite.py` script
The [database_name].xlsx files containing info is saved in the `.\info` folder
```
python .\preprocess\get_info_sqlite.py <db_target_dir>
```
3. generate tables.json
run `.\preprocess\table.py` script, the tables.json and [database_name].db files will be output into `.\data` directory.
```
python .\preprocess\table.py <info_dir> <db_source_dir>
```
4. generate generative_schema.json
git bash run `./src/batch_generate_schema.sh` 
```
./src/batch_generate_schema.sh ./data/
```

## Generate SQLs
Run `.\src\synthetic_data\generate_data_my.py` script
```
python .\src\synthetic_data\generate_data_my.py <template_level: simple|complex>
```