from orchestrator.client import *
from datetime import datetime
from databases.db import Database
from department.department import Department
from databases.alchemy import *
from config.googleapi import *
import json
import csv
import io
import pandas as pd


class Update:
    def __init__(self) -> None:
        pass

    def update_applicant(self, client):
        if not client.applicant_subscribed:
            return
        else:
            if self.time_diff(client.applicant_data_last_update, client.data_update_period):
                print(f"client{client.name}  app needs to update")
            else:
                print(f"client{client.name}  app no need to update")

    def update_department(self, client):
        if not client.department_subscribed:
            return
        else:
            if self.time_diff(client.department_data_last_update, client.data_update_period):
                print(f"client{client.name}  dep needs to update")
                Database.create_db(client, "department")
                dep = Department
                dep.get_info_from_sheet(dep, client.client_data_sheet_link, client.name)
                output_value = "output_test.json"
                db =self.filtering_json(output_value, client.name)
                db.create_view("viewname", "SELECT * FROM peers")
                rows = db.select_view("viewname")
                df = pd.DataFrame(rows)
                csv_buffer = io.BytesIO()
                df.to_csv(csv_buffer, index=False, mode='w')
                csv_buffer.seek(0)
                apiclient = GoogleAPIClient()
                auth = apiclient.authenticate()
                apiservice = GoogleServices(auth)
                apiservice.save_csv(client.name, csv_buffer)

            else:
                print(f"client{client.name}  dep no need to update")

    def update_journal(self, client):
        if not client.journal_subscribed:
            return
        else:
            if self.time_diff(client.journal_data_last_update, client.data_update_period):
                print(f"client{client.name}  jour needs to update")
            else:
                print(f"client{client.name}  jour no need to update")

    def time_diff(lastdate, period):
        cur_time = datetime.now()
        print(" cur_time: ",  cur_time)
        print(" last_date: ",  lastdate)
        last_date = datetime.strptime(lastdate, '%Y-%m-%d %H:%M:%S')
        if period == "monthly":
            period_day = 30
        elif period == "quarterly":
            period_day = 90
        elif period == "yearly":
            period_day = 365
        elif period == "manual":
            period_day = 0
        else:
            print("err with period: ", period)
            return
        if (cur_time - last_date).total_seconds() > period_day * 86400:
            return True
        return

    def filtering_json(json_file_path, db_name):
        with open(json_file_path, 'r', encoding='utf-16') as file:
            data = json.load(file)
        db_path = "./databases/" + db_name + ".db"
        sqlite_db = DatabaseAlc(db_path)
        session = sqlite_db.create_session()
        profile_id = None
        if 'person' in data:
            person_data = data['person']
            profile_id = sqlite_db.insert_data_from_json_main(person_data, ProfileLevelAttribute, session)
        if 'coauthors' in data['person']:
            coauthor_data = data['person']['coauthors']
            sqlite_db.insert_data_from_json_nested(coauthor_data, Coauthor, session,None, profile_id)
        if 'publications' in data['person']:
            publication_data = data['person']['publications']
            sqlite_db.insert_data_from_json_nested(publication_data, Publication, session,None, profile_id)
            for publication in publication_data:
                if 'yearly_citations' in publication:
                    yearly_citations_data = publication['yearly_citations']
                    scholar_id  = publication.get('google_scholar_id', None)
                    pub_id  = publication.get('publicationid', None)
                    sqlite_db.insert_data_from_json_nested(yearly_citations_data, YearlyCitation, session,scholar_id, None, pub_id)
        return sqlite_db
