#databases/db.py
import os
import sqlite3
from pathlib import Path
from  databases.alchemy import *
class Database:
    column_name_list_academician="id INTEGER PRIMARY KEY", "name TEXT", "googlescholarid INT"
    column_name_list_uni="id INTEGER PRIMARY KEY", "name TEXT", "googlelink TEXT"
    column_name_list_setup = 'id INTEGER PRIMARY KEY'

    def __init__(self, name):
        self.database_name = f"{name}.db"
        self.name = name
        print("self from database: ",vars(self))

    def create_setup_db(self):
        db_path = Path("./orchestrator", self.database_name)
        if not db_path.exists():
            print(f"{self.database_name} not found. Creating a new one...")
            db_path.touch()
            print(f"{self.database_name} created.")
            Database.execute_sql_query(self,"databases/create_table_citedbys.sql" , db_path)
        else:
            print("SQLite file found.")
    def create_db(self, subject):
        db_path = Path("./databases", self.name + ".db")
        if not db_path.exists():
            print("SQLite file not found. Creating a new one...")
            db_path.touch()
            print("SQLite file created.")
            if subject=="department":
                db = DatabaseAlc(db_path)
                Base_Academics.metadata.create_all(db.engine)
                return db
            if subject=="journal":
                db = DatabaseAlc(db_path)
                Base_Journal.metadata.create_all(db.engine)
                return db
        else:
            print("SQLite file found.")
    def execute_sql_query(self,file ,path):
                with sqlite3.connect(path) as connection:
                    cursor = connection.cursor()
                    with open(file, 'r') as file:
                            sql_queries = file.read()
                            queries = sql_queries.split(";")
                            for query in queries:
                                if query.strip():
                                    cursor.execute(query)
