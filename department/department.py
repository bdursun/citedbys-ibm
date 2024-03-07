# department/department.py
from databases.db import Database
from config.googleapi import GoogleAPIClient, GoogleServices
from databases.alchemy import *
import gspread


class Department:

    def __init__(self) -> None:
        pass

    def create_subscription(self, client):
        Database(client.name).create_db("department")
        apiclient = GoogleAPIClient()
        auth = apiclient.authenticate()
        apiservice = GoogleServices(auth)
        return apiservice.create_sheet_copy("CitedBys Academic Data Entry Template", client.name, client.email)

    def get_provided_details(self, client):
        db_path = "./databases/db/" + client.name + ".db"
        sqlite_db = DatabaseAlc(db_path)
        session = sqlite_db.create_session()
        apiclient = GoogleAPIClient()
        gc = apiclient.auth_for_gspread()
        sheet = gc.open_by_url(client.client_data_sheet_link)
        if client.department_subscribed:
            sqlite_db.insert_provided_data(
                sheet.get_worksheet(0), DegreesUsed, session)
            sqlite_db.insert_provided_data(
                sheet.get_worksheet(1), DepartmentPeople, session)
            sqlite_db.insert_provided_data(
                sheet.get_worksheet(2), DegreeDates, session)
            print("department added")
        if client.peer_subscribed:
            sqlite_db.insert_provided_data(
                sheet.get_worksheet(3), Peers, session)
            print("peer added")
        if client.applicant_subscribed:
            sqlite_db.insert_provided_data(
                sheet.get_worksheet(4), Applicants, session)
            print("applicant added")

            session.close()
