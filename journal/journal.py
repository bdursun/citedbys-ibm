#journal/journal.py
from databases.alchemy import DatabaseAlc, RejectedPapers
from databases.db import Database
from config.googleapi import GoogleAPIClient, GoogleServices
class Journal:

    def __init__(self) -> None:
        pass
    def create_sheet(self, client):
        Database.create_db(client, "journal")
        apiclient = GoogleAPIClient()
        auth = apiclient.authenticate()
        apiservice=GoogleServices(auth)
        return apiservice.create_sheet_copy("CitedBys Journal Data Entry Template", client.name, client.email)
    def get_info_from_sheet(self, client):
        db_path = "./databases/" + client.name + ".db"
        sqlite_db = DatabaseAlc(db_path)
        session = sqlite_db.create_session()
        apiclient = GoogleAPIClient()
        gc = apiclient.auth_for_gspread()
        sheet = gc.open_by_url(client.client_data_sheet_link)
        apiclient = GoogleAPIClient()
        gc = apiclient.auth_for_gspread()
        sheet = gc.open_by_url(client.client_data_sheet_link)
        if client.journal_subscribed:
            sqlite_db.insert_data_from_sheet(
                sheet.get_worksheet(0), RejectedPapers, session)
            print("journal information from sheet added to db")

            session.close()