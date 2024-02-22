#journal/journal.py
from databases.db import Database
from config.googleapi import GoogleAPIClient, GoogleServices
class Journal:

    def __init__(self, client):
        Database.create_db(client, "journal")
        apiclient = GoogleAPIClient()
        auth = apiclient.authenticate()
        apiservice=GoogleServices(auth)
        self.sheetlink = apiservice.create_sheet_copy("CitedBys Journal Data Entry Template", client.name, client.email)
