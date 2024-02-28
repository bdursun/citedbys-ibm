import sqlite3
import datetime
import time
from department.department import Department
from applicant.applicant import Applicant
from journal.journal import Journal
from orchestrator.update import Update
import config.googleapi


class Client:
    def __init__(self, email, name,
                 short_name, department_name="",
                 department_short_name="",
                 status="new",
                 created=None,
                 client_data_sheet_link="",
                 department_subscribed=0,
                 applicant_subscribed=0,
                 journal_subscribed=0,
                 department_data_last_update="",
                 applicant_data_last_update="",
                 journal_data_last_update="",
                 data_update_period="monthly"):
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
        self.journal_subscribed = journal_subscribed
        self.department_data_last_update = department_data_last_update
        self.applicant_data_last_update = applicant_data_last_update
        self.journal_data_last_update = journal_data_last_update
        self.data_update_period = data_update_period

    # ------------------------------------------------------------------------------------------------------#
    # def __init__(self):
    #     self.name = "web of science"
    #     self.shortname = "wos"
    #     self.sub = "journal"
    #     self.period = "once"
    #     self.email = "infomergeuk16@gmail.com"
    #     self.googlelink = ""
    #     self.lastupdated = datetime.datetime.now()
    # ------------------------------------------------------------------------------------------------------#

    def create_client(self):
        print(vars(self))
        if self.applicant_subscribed:
            self.client_data_sheet_link = Applicant(
                self).sheetlink["webViewLink"]
        if self.department_subscribed:
            dep= Department
            self.client_data_sheet_link = dep.create_sheet(dep,self)["webViewLink"]
        if self.journal_subscribed:
            self.client_data_sheet_link = Journal(
                self).sheetlink["webViewLink"]

        conn = sqlite3.connect('./orchestrator/citedbys.db')
        cursor = conn.cursor()
        insert_query = '''INSERT INTO client_informations ( email, name,
                 short_name, department_name,
                 department_short_name,
                 status,created,client_data_sheet_link,
                 department_subscribed ,
                 applicant_subscribed,
                 journal_subscribed,
                 department_data_last_update,
                 applicant_data_last_update,
                 journal_data_last_update,
                 data_update_period) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)'''
        cursor.execute(insert_query, (self.email, self.name, self.short_name, self.department_name, self.department_short_name, self.status,  time.time(), self.client_data_sheet_link, self.department_subscribed,
                       self.applicant_subscribed, self.journal_subscribed, self.department_data_last_update, self.applicant_data_last_update, self.journal_data_last_update, self.data_update_period))
        conn.commit()
        print("Value updated successfully")
        conn.close()

    def get_client_info(id):
        conn = sqlite3.connect('./orchestrator/citedbys.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM client_informations WHERE id=?", (id,))
            selected_data = cursor.fetchone()
            if selected_data:
                print("Selected data:", selected_data)
                return selected_data
            else:
                print("No data found with the specified ID")
                return None
        finally:
            conn.close()

    def get_all_client_info():
        conn = sqlite3.connect('./orchestrator/citedbys.db')
        cursor = conn.cursor()
        selected_data = ""
        try:
            cursor.execute("SELECT * FROM client_informations")
            selected_data = cursor.fetchall()
            if selected_data:
                for data in selected_data:
                    print("client: ", data)
            else:
                print("No data found")
        finally:
            conn.close()
            return selected_data

    def remove_client(id):
        conn = sqlite3.connect('./orchestrator/citedbys.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tablename WHERE id=?", (id,))
            conn.commit()
            print("Client removed successfully")
        finally:
            conn.close()

    def remove_everyone(tablename):
        conn = sqlite3.connect('')
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {tablename}")
            conn.commit()
            print(f"Everyone removed from {tablename} successfully")
        finally:
            conn.close()

    def remove_table(tablename):
        conn = sqlite3.connect('./orchestrator/citedbys.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {tablename}")
            conn.commit()
            print(f"Table: {tablename} removed successfully")
        finally:
            conn.close()

    def update_client_information(id, column, value):
        conn = sqlite3.connect('./orchestrator/citedbys.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"UPDATE client_informations SET {column}=? WHERE id=?", (value, id))
            conn.commit()
            print("Value updated successfully")
        finally:
            conn.close()

    def daily_update(self):
        update = Update
        clients = self.get_all_client_info()
        for index, client in enumerate(clients):
            try:
                index_, *client_without_id = client
                classClient = Client(*client_without_id)
            except Exception as e:
                print(
                    f"Error occurred while creating Client object for client at index {index}: {e}")
            if classClient.department_subscribed or classClient.applicant_subscribed or classClient.journal_subscribed:

                if classClient.department_subscribed:
                    update.update_department(Update, classClient)
                if classClient.applicant_subscribed:
                    update.update_applicant(Update, classClient)
                if classClient.journal_subscribed:
                    update.update_journal(Update, classClient)
            else:
                print(f"couldnt find any sub for {classClient.name}")

    def manual_update(self, id):
        update = Update
        client = self.get_client_info(id)
        try:
            id_, *client_without_id = client
            classClient = Client(*client_without_id)
        except Exception as e:
            print(
                f"Error occurred while creating Client object for client at index {id}: {e}")
        if classClient.department_subscribed or classClient.applicant_subscribed or classClient.journal_subscribed:
            if classClient.department_subscribed:
                update.update_department(Update, classClient)
            if classClient.applicant_subscribed:
                update.update_applicant(Update, classClient)
            if classClient.journal_subscribed:
                update.update_journal(Update, classClient)
        else:
            print(f"couldnt find any sub for {classClient.name}")
