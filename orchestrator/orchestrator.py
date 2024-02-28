# orchestrator/orchestrator.py
import os
import time
from databases.db import Database
from orchestrator.client import Client
import sys


def create_client(email, name, short_name="", department_name="", department_short_name="", status="new", client_data_sheet_link="", department_subscribed=0, applicant_subscribed=0, journal_subscribed=0, department_data_last_update="", applicant_data_last_update="", journal_data_last_update="", data_update_period="one_demand"):
    print(email)
    client = Client(email, name, short_name, department_name, department_short_name, status,None ,client_data_sheet_link, department_subscribed, applicant_subscribed, journal_subscribed, department_data_last_update, applicant_data_last_update, journal_data_last_update, data_update_period)
    client.create_client()

def get_info_client(id):
    Client.get_client_info(id)


def get_all_info_client():
    Client.get_all_client_info()


def remove_client(id):
    Client.remove_client(id)


def remove_everyone(tablename):
    Client.remove_everyone(tablename)


def remove_table(tablename):
    Client.remove_table(tablename)

def update_client_information(id, column, value):
    Client.update_client_information(id,column, value)

def daily_update():
    Client.daily_update(Client)

def manual_update(id):
    Client.manual_update(Client, id)
