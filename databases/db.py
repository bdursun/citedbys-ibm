#databases/db.py
import os
import sqlite3
from pathlib import Path
class Database:
    column_name_list_academician="id INTEGER PRIMARY KEY", "name TEXT", "googlescholarid INT"
    column_name_list_uni="id INTEGER PRIMARY KEY", "name TEXT", "googlelink TEXT"

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
            Database.create_table(self, "tablename", Database.column_name_list_uni, db_path)
        else:
            print("SQLite file found.")
    def create_db(self, subject):
        print("createdb:", vars(self))
        db_path = Path("./databases", self.name + ".db")
        if not db_path.exists():
            print("SQLite file not found. Creating a new one...")
            db_path.touch()
            print("SQLite file created.")
            if subject=="applicant":
                #applicant db create procedure
                Database.create_table(self, "tablename", Database.column_name_list_academician, db_path)
            if subject=="department":
                #department db create procedure
                Database.create_table(self,"academician", Database.column_name_list_academician, db_path)

            if subject=="journal":
                #journal db create procedure
                Database.create_table(self,"tablename",   Database.column_name_list_academician, db_path)
        else:
            print("SQLite file found.")
    def create_table(self, table_name, columns, path):
            with sqlite3.connect(path) as connection:
                cursor = connection.cursor()
                create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
                cursor.execute(create_table_sql)
                print(f"Table '{table_name}' created with columns: {', '.join(columns)}")
