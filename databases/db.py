# databases/db.py
import os
from pathlib import Path
from databases.alchemy import *


class Database:
    def __init__(self, name):
        self.database_name = f"{name}.db"
        self.name = name
        print("self from database: ", vars(self))

    def create_db(self, subject):
        db_path = Path("./databases/db/", self.database_name)
        if not db_path.exists():
            print(f"{self.database_name} not found. Creating a new one...")
            db_path.touch()
            print(f"{self.database_name} created.")
            db = DatabaseAlc(db_path)
            table = academic_tables if subject == "department" else journal_tables
            tables = [Base.metadata.tables[table_name] for table_name in table]
            Base.metadata.create_all(db.engine, tables=tables)
            return db
        else:
            print("SQLite file found.")

    def create_setup_db(self):
        db_path = Path("./orchestrator/db", self.database_name)
        if not db_path.exists():
            print(f"{self.database_name} not found. Creating a new one...")
            db_path.touch()
            print(f"{self.database_name} created.")
            setup_tables = [Base.metadata.tables[table_name]
                            for table_name in setup_table]
            db = DatabaseAlc(db_path)
            Base.metadata.create_all(db.engine, tables=setup_tables)
        else:
            print("SQLite file found.")
