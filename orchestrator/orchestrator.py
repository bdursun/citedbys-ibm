# orchestrator/orchestrator.py
import os
import time
from databases.db import Database
from databases.alchemy import *

from orchestrator.client import Client
import sys


class Orchestrator:
    @staticmethod
    def create_client(email, name, short_name="", department_name="", department_short_name="", status="new", created=None, client_data_sheet_link="", department_subscribed=0, applicant_subscribed=0, peer_subscribed=0, journal_subscribed=0, department_data_last_update="", journal_data_last_update="", data_update_period="one_demand"):
        print(email)
        client = Client(email, name, "", short_name, department_name, department_short_name, status, created, client_data_sheet_link, department_subscribed,
                        applicant_subscribed, peer_subscribed, journal_subscribed, department_data_last_update, journal_data_last_update, data_update_period)
        client.create_client()

    @staticmethod
    def get_info_client(id):
        return DatabaseAlc('orchestrator/db/citedbys.db').get_client_info(id)

    @staticmethod
    def get_all_info_client():
        return DatabaseAlc('orchestrator/db/citedbys.db').get_all_client_info()

    @staticmethod
    def remove_one_client(id):
        DatabaseAlc('orchestrator/db/citedbys.db').remove_one_client(id)

    @staticmethod
    def remove_all_client():
        DatabaseAlc('orchestrator/db/citedbys.db').remove_all_client()

    @staticmethod
    def update_client_information(id, column, value):
        DatabaseAlc(
            'orchestrator/db/citedbys.db').update_client_information(id, column, value)

    @staticmethod
    def daily_update():
        Client.daily_update(Client)

    @staticmethod
    def manual_update(id):
        Client.manual_update(Client, id)
