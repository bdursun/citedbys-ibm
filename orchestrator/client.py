# databases/client.py
from pathlib import Path
import sqlite3
import datetime
import time
from department.department import Department
from journal.journal import Journal
from orchestrator.update import Update
from databases.alchemy import DatabaseAlc
import config.googleapi


class Client:
    def __init__(self, email, name,
                id="",short_name="", department_name="",
                 department_short_name="",
                 status="new",
                 created=None,
                 client_data_sheet_link="",
                 department_subscribed=0,
                 applicant_subscribed=0,
                 peer_subscribed=0,
                 journal_subscribed=0,
                 department_data_last_update="",
                 journal_data_last_update="",
                 data_update_period="monthly"):
        if id != "":
            self.id = id
        self.email = email
        self.name = name
        self.short_name = short_name
        self.department_name = department_name
        self.department_short_name = department_short_name
        self.status = status
        self.created = created
        self.client_data_sheet_link = client_data_sheet_link
        self.department_subscribed = department_subscribed
        self.applicant_subscribed = applicant_subscribed
        self.peer_subscribed = peer_subscribed
        self.journal_subscribed = journal_subscribed
        self.department_data_last_update = department_data_last_update
        self.journal_data_last_update = journal_data_last_update
        self.data_update_period = data_update_period

    def create_client(self):
        print(vars(self))
        if self.department_subscribed:
            dep = Department()
            self.client_data_sheet_link = dep.create_subscription(self)[
                "webViewLink"]
        if self.journal_subscribed:
            jour = Journal()
            self.client_data_sheet_link = jour.create_subscription(self)[
                "webViewLink"]

        db_path = Path('orchestrator/db/citedbys.db')
        sqlite_db = DatabaseAlc(db_path)
        sqlite_db.insert_data_for_creating_client(self)

    def daily_update(self):
        update = Update()
        sqlite_db = DatabaseAlc('orchestrator/db/citedbys.db')
        clients = sqlite_db.get_all_client_info()
        for index, client in enumerate(clients):
            try:
                client_attributes = client.__dict__
        # Remove the '_sa_instance_state' key from the dictionary
                client_attributes.pop('_sa_instance_state', None)
                classClient = Client(**client_attributes)
            except Exception as e:
                print(f"Error occurred while creating Client object: {e}")
            if classClient.department_subscribed or classClient.peer_subscribed or classClient.applicant_subscribed or classClient.journal_subscribed:
                if classClient.journal_subscribed:
                    update.update_journal(classClient)
                else:
                    update.update_department(classClient)
            else:
                print(f"couldnt find any sub for {classClient.name}")

    def manual_update(self, id):
        update = Update()
        sqlite_db = DatabaseAlc('orchestrator/db/citedbys.db')
        client = sqlite_db.get_client_info(id)
        print(vars(client))
        try:
            client_attributes = client.__dict__
    # Remove the '_sa_instance_state' key from the dictionary
            client_attributes.pop('_sa_instance_state', None)
            classClient = Client(**client_attributes)
            print(vars(classClient))
            print('department subs: ',classClient.department_subscribed)
        except Exception as e:
            print(f"Error occurred while creating Client object: {e}")
        if classClient.department_subscribed or classClient.peer_subscribed or classClient.applicant_subscribed or classClient.journal_subscribed:
            if classClient.journal_subscribed:
                update.update_journal(classClient)
            else:
                update.update_department(classClient)
        else:
            print(f"couldnt find any sub for {classClient.name}")
