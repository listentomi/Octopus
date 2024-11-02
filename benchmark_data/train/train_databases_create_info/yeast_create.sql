CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE Genes
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  name TEXT UNIQUE);
CREATE TABLE locations 
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  location TEXT UNIQUE);
CREATE TABLE Molecular
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  function TEXT UNIQUE);
CREATE TABLE Bioprocess 
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                process TEXT UNIQUE);
CREATE TABLE Member (
            gene_id INTEGER,
            location_id INTEGER,
            function_id INTEGER,
            bioprocess_id INTEGER,
            PRIMARY KEY (gene_id,location_id,function_id,bioprocess_id));
CREATE TABLE Treatment (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        condition TEXT UNIQUE);
CREATE TABLE Description (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        meaning TEXT UNIQUE);
CREATE TABLE Relation (
                        condition_id INTEGER,
                        meaning_id INTEGER,
                        PRIMARY KEY (condition_id,meaning_id));
CREATE TABLE Expression (           
                gene_id INTEGER,
                transcripts INTEGER,
                  treatment_id INTEGER,
                  location_id INTEGER,
                  meaning_id INTEGER,
                  function_id INTEGER,
                  bioprocess_id INTEGER);
