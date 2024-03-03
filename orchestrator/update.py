from orchestrator.client import *
from datetime import datetime
from databases.db import Database
from department.department import Department
from databases.alchemy import *
from config.googleapi import *
from crawler.crawler import *
import json
import csv
import io
import pandas as pd
import os


class Update:
    def __init__(self) -> None:
        pass

    def update_department(self, client):
        if not client.department_subscribed and client.peer_subscribed and client.applicant_subscribed:
            return
        else:
            if self.time_diff(client.department_data_last_update, client.data_update_period):
                print(f"client{client.name}  dep needs to update")
                self.update_client_data(client, 'department')
                self.create_view_and_save_csv(client, 'SELECT * FROM peers')
                # call crawler class and return outputvalue

            else:
                print(f"client{client.name}  dep no need to update")

    def update_journal(self, client):
        if not client.journal_subscribed:
            return
        else:
            if self.time_diff(client.journal_data_last_update, client.data_update_period):
                print(f"client{client.name}  jour needs to update")
                self.update_client_data(client, "journal")
                self.create_view_and_save_csv(
                    client, 'SELECT * FROM matched_publications')
            else:
                print(f"client{client.name}  jour no need to update")

    def time_diff(self, lastdate, period):
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

    def filtering_json(self, json_file_path, client):
        with open(json_file_path, 'r', encoding='utf-16') as file:
            data = json.load(file)
        db_path = "./databases/" + client.name + ".db"
        sqlite_db = DatabaseAlc(db_path)
        session = sqlite_db.create_session()
        profile_id = None
        if client.department_subscribed or client.applicant_subscribed or client.peer_subscribed:
            if 'person' in data:
                person_data = data['person']
                profile_id = sqlite_db.insert_data_from_json_main(
                    person_data, ProfileLevelAttribute, session)
            if 'coauthors' in data['person']:
                coauthor_data = data['person']['coauthors']
                sqlite_db.insert_data_from_json_nested(
                    coauthor_data, Coauthor, session, None, profile_id)
            if 'publications' in data['person']:
                publication_data = data['person']['publications']
                sqlite_db.insert_data_from_json_nested(
                    publication_data, Publication, session, None, profile_id)
                for publication in publication_data:
                    if 'yearly_citations' in publication:
                        yearly_citations_data = publication['yearly_citations']
                        scholar_id = publication.get('google_scholar_id', None)
                        pub_id = publication.get('publicationid', None)
                        sqlite_db.insert_data_from_json_nested(
                            yearly_citations_data, YearlyCitation, session, scholar_id, None, pub_id)
            return sqlite_db
        if client.journal_subscribed:
            if 'matched_publications' in data:
                for journal_data in data['matched_publications']:
                    sqlite_db.insert_data_from_json_main(
                        journal_data, MatchedPublications, session)
            return sqlite_db

    def delete_last_db(self, name):
        file_path = f'./databases/{name}.db'
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been successfully deleted.")
        else:
            print(f"File '{file_path}' does not exist.")

    def crawling_loop(self, client):
        db_path = "./databases/" + client.name + ".db"
        sqlite_db = DatabaseAlc(db_path)
        session = sqlite_db.create_session()
        crawler_class = Crawler()
        if client.department_subscribed or client.peer_subscribed or client.applicant_subscribed:
            departments = session.query(DepartmentPeople)
            if departments:
                for department in departments:
                    result = crawler_class.execute_crawler('department',
                                                           department.google_scholar_id)
                    print(result)
            peers = session.query(Peers)
            if peers:
                for peer in peers:
                    result = crawler_class.execute_crawler(
                        'department', peer.google_scholar_id)
                    print(result)
            applicants = session.query(Applicants)
            if applicants:
                for applicant in applicants:
                    result = crawler_class.execute_crawler('department',
                                                           applicant.applicant_google_scholar_id)
                    print(result)
        else:
            rejected_papers = session.query(RejectedPapers)
            if rejected_papers:
                for rejected_paper in rejected_papers:
                    print(rejected_paper.traceid)
                    result = crawler_class.execute_crawler('journal',
                                                           rejected_paper.traceid)  # it will change to needed parameters for crawler
                    print(result)

    def update_client_data(self, client, subject):
        self.delete_last_db(client.name)
        Database.create_db(client, subject)
        if subject == "department":
            dep = Department()
            dep.get_info_from_sheet(client)
        else:
            jour = Journal()
            jour.get_info_from_sheet(client)
        self.crawling_loop(client)  # it will return json data

    def create_view_and_save_csv(self, client, query):
        db = self.filtering_json("journal template.json", client)
        db.create_view("viewname", query)
        rows = db.select_view("viewname")
        df = pd.DataFrame(rows)
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False, mode='w')
        csv_buffer.seek(0)
        apiclient = GoogleAPIClient()
        auth = apiclient.authenticate()
        apiservice = GoogleServices(auth)
        apiservice.save_csv(client.name, csv_buffer)
