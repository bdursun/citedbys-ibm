#orchestrator/orchestrator.py
import os
from databases.db import Database
from orchestrator.client import Client
import sys
def setup():
        print("Installing Python dependencies...")
        os.system("pip install -r requirements.txt")
        print("Dependencies installed.")
        #db check
        Database("citedbys").create_setup_db()

def create_client(name, shortname, sub, period, email, googlelink):
     Client.create_client(name, shortname, sub, period, email, googlelink)

def management():
    print("Client features")
    while True:
        action = input("Type 'clientid', 'add' to add a new client, 'back' to go back to the menu, or 'exit' to quit: ").strip()
        if action == 'add':
                Client.create_client(Client())
                print("New client added successfully.")

        elif action == 'back':
            print("Returning to the menu...")
            break

        elif action == 'exit':
            print("Exiting...")
            sys.exit()

        else:
            #try to find client from id
            try:
                 int(action)
                 print("int")
            except ValueError:
                 print("not integer")


def check():
        print("checking&updating")