#department/department.py
from databases.db import Database
from config.googleapi import GoogleAPIClient, GoogleServices
class Department:

    def __init__(self, client):
        Database.create_db(client, "department")
        apiclient = GoogleAPIClient()
        auth = apiclient.authenticate()
        apiservice=GoogleServices(auth)
        self.sheetlink = apiservice.create_sheet_copy("CitedBys Academic Data Entry Template", client.name, client.email)
