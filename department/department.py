# department/department.py
from databases.db import Database
from config.googleapi import GoogleAPIClient, GoogleServices
from databases.alchemy import *
import gspread
import sqlite3


class Department:

    def __init__(self) -> None:
        pass

    def create_sheet(self, client):
        Database.create_db(client, "department")
        apiclient = GoogleAPIClient()
        auth = apiclient.authenticate()
        apiservice = GoogleServices(auth)
        return apiservice.create_sheet_copy("CitedBys Academic Data Entry Template", client.name, client.email)

    def get_info_from_sheet(self, link, db_name):
        db_path = "./databases/" + db_name + ".db"
        sqlite_db = DatabaseAlc(db_path)
        session = sqlite_db.create_session()
        apiclient = GoogleAPIClient()
        gc = apiclient.auth_for_gspread()
        sheet = gc.open_by_url(link)
        apiclient = GoogleAPIClient()
        gc = apiclient.auth_for_gspread()
        sheet = gc.open_by_url(link)
        sqlite_db.insert_data_from_sheet(
            sheet.get_worksheet(0), DegreesUsed, session)
        sqlite_db.insert_data_from_sheet(
            sheet.get_worksheet(1), DepartmentPeople, session)
        sqlite_db.insert_data_from_sheet(
            sheet.get_worksheet(2), DegreeDates, session)
        sqlite_db.insert_data_from_sheet(
            sheet.get_worksheet(3), Peers, session)
        sqlite_db.insert_data_from_sheet(
            sheet.get_worksheet(4), Applicants, session)
        session.close()

        # conn = sqlite3.connect(f'./databases/{db_name}.db')
        # cursor = conn.cursor()
        # print(page_0)
        # for a_row in page_0.get_all_records():
        #     print(a_row)
        #     insert_query = '''INSERT INTO degrees_used ( degree_name, degree_short_name,
        #             degree_rank) VALUES (?, ?, ?)'''
        #     cursor.execute(
        #         insert_query, (a_row['Degree Name'], a_row['Degree Short Name'], a_row['Degree Rank']))
        #     conn.commit()
        # page_1 = sheet.get_worksheet(1)
        # cursor = conn.cursor()
        # for a_row in page_1.get_all_records():
        #     insert_query = '''INSERT INTO department_people ( current_degree, person_full_name,
        #             google_scholar_profile_link,google_scholar_id,department_join_date  ) VALUES (?, ?, ?, ? , ?)'''
        #     cursor.execute(insert_query, (a_row['Current Degree'], a_row['Person Full Name'],
        #                    a_row['Google Scholar Profile Link'], a_row['GoogleScholarID'], a_row['Department Join Date']))
        #     conn.commit()
        # page_2 = sheet.get_worksheet(2)
        # cursor = conn.cursor()
        # for a_row in page_2.get_all_records():
        #     insert_query = '''INSERT INTO degree_dates ( person_name, degree,
        #             degree_date) VALUES (?, ?, ?)'''
        #     cursor.execute(
        #         insert_query, (a_row['Person Name'], a_row['Degree'], a_row['Degree Date']))
        #     conn.commit()
        # page_3 = sheet.get_worksheet(3)
        # cursor = conn.cursor()
        # for a_row in page_3.get_all_records():
        #     insert_query = '''INSERT INTO peers ( university_name, department_name,
        #             degree,full_name , google_scholar_profile_link, google_scholar_id) VALUES (?, ?, ?, ?, ?, ?)'''
        #     cursor.execute(
        #         insert_query, (a_row['University Name'], a_row['Department Name'], a_row['Degree'],a_row['Fullname'], a_row['Google Scholar Profile Link'], a_row['Google Scholar ID']))
        #     conn.commit()
        # page_4 = sheet.get_worksheet(4)
        # cursor = conn.cursor()
        # for a_row in page_4.get_all_records():
        #     insert_query = '''INSERT INTO applicants ( degree, full_name,
        #             gs_profile_url, google_scholar_id) VALUES (?, ?, ?, ?)'''
        #     cursor.execute(
        #         insert_query, (a_row['Applicant Degree'], a_row['Applicant Full Name'], a_row['Applicant Google Scholar Profile Link'], a_row['Applicant Google Scholar ID']))

        #     conn.commit()
        # page_1 = sheet.get_worksheet(0)
        # cursor = conn.cursor()
        # for a_row in page_1:
        #     insert_query = '''INSERT INTO degrees_used ( degree_name, degree_short_name,
        #             degree_rank) VALUES (?, ?, ?)'''
        #     cursor.execute(insert_query, (a_row['Degree Name'], a_row['Degree Short Name'],a_row['Degree Rank']))
        #     conn.commit()

        # conn.close()

        # sheets = sheet.worksheets()
        # for worksheet in sheets:
        #     records = worksheet.get_all_records()
        #     print(records, '\n')
