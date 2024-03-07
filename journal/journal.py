# journal/journal.py
from databases.alchemy import DatabaseAlc, RejectedPapers
from databases.db import Database
from config.googleapi import GoogleAPIClient, GoogleServices


class Journal:

    def __init__(self) -> None:
        pass

    def create_subscription(self, client):
        Database(client.name).create_db("journal")
        apiclient = GoogleAPIClient()
        auth = apiclient.authenticate()
        apiservice = GoogleServices(auth)
        return apiservice.create_sheet_copy("CitedBys Journal Data Entry Template", client.name, client.email)

    def get_provided_details(self, client):
        db_path = "./databases/db/" + client.name + ".db"
        sqlite_db = DatabaseAlc(db_path)
        session = sqlite_db.create_session()
        apiclient = GoogleAPIClient()

        gc = apiclient.auth_for_gspread()
        sheet = gc.open_by_url(client.client_data_sheet_link)
        if client.journal_subscribed:
            sqlite_db.insert_provided_data(
                sheet.get_worksheet(0), RejectedPapers, session)
            print("journal information from sheet added to db")
            session.close()
