import sqlite3
import datetime
from department.department import Department
from applicant.applicant import Applicant
from journal.journal import Journal

import config.googleapi


class Client:
    # def __init__(self, name, shortname, sub, period, email, googlelink=""):
    #     self.name= name
    #     self.shortname= shortname
    #     self.sub= sub
    #     self.period= period
    #     self.email= email
    #     self.googlelink= googlelink

    # ------------------------------------------------------------------------------------------------------#
    def __init__(self):
        self.name = "web of science"
        self.shortname = "wos"
        self.sub = "journal"
        self.period = "once"
        self.email = "infomergeuk16@gmail.com"
        self.googlelink = ""
        self.lastupdated = datetime.datetime.now()
    # ------------------------------------------------------------------------------------------------------#

    def create_client(self):
        # --#
        # config.googleapi.newSheet("CitedBys Academic Data Entry Template", self.name)
        # --#
        all_subs = self.sub.split("+")
        for ind_sub in all_subs:
            if ind_sub == "applicant":
                self.googlelink = Applicant(self).sheetlink["webViewLink"]
            elif ind_sub == "department":
                self.googlelink = Department(self).sheetlink["webViewLink"]
            elif ind_sub == "journal":
                self.googlelink = Journal(self).sheetlink["webViewLink"]

        conn = sqlite3.connect('./orchestrator/citedbys.db')
        cursor = conn.cursor()
        insert_query = '''INSERT INTO tablename (name, googlelink) VALUES (?, ?)'''
        cursor.execute(insert_query, (self.name, self.googlelink))
        conn.commit()
