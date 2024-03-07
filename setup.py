# setup.py
import os
from databases.db import Database
print("Installing Python dependencies...")
os.system("pip install -r requirements.txt")
print("Dependencies installed.")
Database("citedbys").create_setup_db()
