# databases/alchemy.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, DateTime, ForeignKeyConstraint, MetaData, create_engine, Column, Integer, String, ForeignKey, func, select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import csv
import pandas as pd

Base = declarative_base()
academic_tables = ['profile_level_attributes', 'peers', 'degrees_used', 'department_people',
                   'degree_dates', 'applicants', 'coauthors', 'publications', 'yearly_citations']
journal_tables = ['matched_publications', 'rejected_papers']
setup_table = ['client_informations']


class DatabaseAlc:
    def __init__(self, db_path):
        db_url = 'sqlite:///' + str(db_path)
        print("url: ", db_url)
        self.engine = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.Session()

    def insert_data_for_creating_client(self, client):
        Session = self.create_session()
        try:
            client_data = ClientInformation(**vars(client))
            print(vars(client_data))
            Session.add(client_data)
            Session.commit()
            print("Client added successfully")
        except Exception as e:
            print(f"CLIENTERRRRRORR: {e}")
            Session.rollback()

    def insert_provided_data(self, sheet, table, session):
        for a_row in sheet.get_all_records():
            try:
                data = {key.replace(' ', '_').lower()
                                    : value for key, value in a_row.items()}
                session.add(table(**data))
                session.commit()
            except Exception as e:
                print(f"Error occurred while inserting data: {e}")
                session.rollback()

    def insert_data_from_json_nested(self, data, table, session, google_scholar_id=None, profile_id=None, publicationid=None):
        try:
            for item in data:
                try:
                    row_data = {}
                    for key, value in item.items():
                        column_name = key.lower().replace(' ', '_')
                        if hasattr(table, column_name):
                            row_data[column_name] = value
                    if google_scholar_id:
                        row_data['google_scholar_id'] = google_scholar_id
                    if profile_id:
                        row_data['profile_level_attributes_id'] = profile_id
                    if publicationid:
                        row_data['publicationid'] = publicationid
                    table_instance = table(**row_data)
                    session.add(table_instance)
                    session.commit()
                except Exception as e:
                    print(
                        f"---------------------------------------------------table:{table} item: {item}  Error occurred while inserting data: {e}")
                    session.rollback()
        except Exception as e:
            print(
                f"--------------------------------------------------table:{table} item: {item}   Error occurred while processing JSON data: {e}")

    def insert_data_from_json_main(self, data, table, session):
        row_data = {}
        for key, values in data.items():
            if not (key == "coauthors" or key == "publications"):
                if key == "profile_header_details" or key == "profile_header_details_links":
                    values = str(values)
                if hasattr(table, key):
                    row_data[key] = values
        table_instance = table(**row_data)
        session.add(table_instance)
        session.commit()
        print(table_instance)
        print('\n')
        return table_instance.id

    def create_view(self, view_name, query):
        with self.engine.connect() as conn:
            conn.execute(text(f"DROP VIEW IF EXISTS {view_name}"))
            conn.execute(text(f"CREATE VIEW {view_name} AS {query}"))
        return view_name

    def select_view(self, view_name):
        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {view_name}"))
            rows = result.fetchall()
            return rows

    def get_client_info(self, id):
        Session = self.create_session()
        return Session.query(ClientInformation).filter_by(id=id).first()

    def get_all_client_info(self):
        Session = self.create_session()
        return Session.query(ClientInformation).all()

    def remove_one_client(self, id):
        Session = self.create_session()

        client = Session.query(ClientInformation).filter_by(id=id).first()
        if client:
            Session.delete(client)
            Session.commit()
            print("Client removed successfully")
        else:
            print("No client found with the specified ID")

    def remove_all_client(self):
        Session = self.create_session()
        Session.query(ClientInformation).delete()
        Session.commit()
        print("Everyone removed from clients successfully")

    def update_client_information(self, id, column, value):
        Session = self.create_session()
        client = Session.query(ClientInformation).filter_by(id=id).first()
        if client:
            setattr(client, column, value)
            Session.commit()
            print("Value updated successfully")
        else:
            print("No client found with the specified ID")


class ProfileLevelAttribute(Base):
    __tablename__ = 'profile_level_attributes'

    id = Column(Integer, primary_key=True)
    google_scholar_id = Column(String(255))
    gs_profile_url = Column(String(255))
    fullname = Column(String(255))
    verified_email = Column(String(255))
    organisation_url = Column(String(255))
    organisation_id = Column(String(255))
    organisation_name = Column(String(255))
    profile_image_url = Column(String(255))
    profile_header_details = Column(String(255))
    profile_header_details_links = Column(String(255))
    citedby_total = Column(Integer)
    h_index = Column(Integer)
    i10_index = Column(Integer)
    last5_citedby_total = Column(Integer)
    last5_h_index = Column(Integer)
    last5_i10_index = Column(Integer)
    title = Column(String(255))
    homepage_url = Column(String(255))
    department_name = Column(String(255))
    department_url = Column(String(255))


class Coauthor(Base):
    __tablename__ = 'coauthors'

    id = Column(Integer, primary_key=True)
    profile_level_attributes_id = Column(
        Integer, ForeignKey('profile_level_attributes.id'))
    google_scholar_id = Column(String(255))
    fullname = Column(String(255))
    organisation_name = Column(String(255))
    profile_image_set = Column(String(255))
    profile_level_attributes = relationship("ProfileLevelAttribute")


class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    profile_level_attributes_id = Column(
        Integer, ForeignKey('profile_level_attributes.id'))
    google_scholar_id = Column(String(255))
    publication_year = Column(Integer)
    citedby_url = Column(String(255))
    total_citations = Column(Integer)
    publication_title = Column(String(255))
    publication_url = Column(String(255))
    publication_publish_url = Column(String(255))
    publicationid = Column(String(255))
    pdf_link = Column(String(255))
    publication_type = Column(String(255))
    issue = Column(String(255))
    authors = Column(String(255))
    publication_date = Column(String(255))
    journal = Column(String(255))
    pages = Column(String(255))
    volume = Column(String(255))
    conference = Column(String(255))
    publisher = Column(String(255))
    patent_office = Column(String(255))
    book_name = Column(String(255))
    citedby_total_url = Column(String(255))
    pdf_text = Column(String(255))
    description = Column(String(255))
    source = Column(String(255))
    profile_level_attributes = relationship("ProfileLevelAttribute")


class YearlyCitation(Base):
    __tablename__ = 'yearly_citations'

    id = Column(Integer, primary_key=True)
    publicationid = Column(Integer, ForeignKey('publications.publicationid'))
    google_scholar_id = Column(Integer, ForeignKey(
        'publications.google_scholar_id'))
    citation_year = Column(Integer)
    citation_count = Column(Integer)
    ForeignKeyConstraint(['publicationid', 'google_scholar_id'], [
                         'publications.publicationid', 'publications.google_scholar_id'])


class Peers(Base):
    __tablename__ = 'peers'

    id = Column(Integer, primary_key=True)
    university_name = Column(String(255))
    department_name = Column(String(255))
    degree = Column(String(255))
    full_name = Column(String(255))
    google_scholar_profile_link = Column(String(255))
    google_scholar_id = Column(String(255))


class DegreesUsed(Base):
    __tablename__ = 'degrees_used'

    id = Column(Integer, primary_key=True)
    degree_name = Column(String(255))
    degree_short_name = Column(String(255))
    degree_rank = Column(Integer)


class DepartmentPeople(Base):
    __tablename__ = 'department_people'

    id = Column(Integer, primary_key=True)
    current_degree = Column(String(255))
    person_full_name = Column(String(255))
    google_scholar_profile_link = Column(String(255))
    google_scholar_id = Column(String(255))
    department_join_date = Column(String(255))


class DegreeDates(Base):
    __tablename__ = 'degree_dates'

    id = Column(Integer, primary_key=True)
    person_name = Column(String(255))
    degree = Column(String(255))
    degree_date = Column(String(255))


class Applicants(Base):
    __tablename__ = 'applicants'

    id = Column(Integer, primary_key=True)
    applicant_degree = Column(String(255))
    applicant_full_name = Column(String(255))
    applicant_google_scholar_profile_link = Column(String(255))
    applicant_google_scholar_id = Column(String(255))


class MatchedPublications(Base):
    __tablename__ = 'matched_publications'

    id = Column(Integer, primary_key=True)
    data_source = Column(String(255))
    match_rank = Column(Integer)
    publication_title = Column(String(255))
    publication_publish_url = Column(String(255))
    pdf_link = Column(String(255))
    pdf_text = Column(String(255))
    publication_year = Column(Integer)
    citedby_url = Column(String(255))
    total_citations = Column(String(255))
    authors = Column(String(255))
    authors_google_scholar_ids = Column(String(255))
    publisher = Column(String(255))
    publicationid = Column(String(255))
    cite_page_text = Column(String(255))
    traceid = Column(Integer)


class RejectedPapers(Base):
    __tablename__ = 'rejected_papers'

    id = Column(Integer, primary_key=True)
    traceid = Column(Integer)
    manuscript_title = Column(String(255))
    authors_list = Column(String(255))
    manuscript_year = Column(Integer)
    keywords = Column(String(255))


class ClientInformation(Base):
    __tablename__ = 'client_informations'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    short_name = Column(String(255))
    department_name = Column(String(255))
    department_short_name = Column(String(255))
    status = Column(String(255), nullable=False, default='new')
    created = Column(DateTime, default=func.current_timestamp())
    client_data_sheet_link = Column(String(255))
    department_subscribed = Column(Boolean, default=False)
    applicant_subscribed = Column(Boolean, default=False)
    peer_subscribed = Column(Boolean, default=False)
    journal_subscribed = Column(Boolean, default=False)
    department_data_last_update = Column(DateTime)
    journal_data_last_update = Column(DateTime)
    data_update_period = Column(String(255))
