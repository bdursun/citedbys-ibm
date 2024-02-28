CREATE TABLE degrees_used(
    id INTEGER PRIMARY KEY ,
    degree_name VARCHAR(255),
    degree_short_name VARCHAR(255),
    degree_rank INT
);

CREATE TABLE department_people(
    id INTEGER PRIMARY KEY ,
    current_degree VARCHAR(255),
    person_full_name VARCHAR(255),
    google_scholar_profile_link VARCHAR(255),
    google_scholar_id VARCHAR(255),
    department_join_date DATETIME
);

CREATE TABLE degree_dates(
    id INTEGER PRIMARY KEY ,
    person_name VARCHAR(255),
    degree VARCHAR(255),
    degree_date DATETIME
);