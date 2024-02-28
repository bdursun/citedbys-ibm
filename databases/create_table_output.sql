CREATE TABLE profile_level_attributes(
    id INTEGER PRIMARY KEY,
    google_scholar_id VARCHAR(255),
    gs_profile_url VARCHAR(255),
    fullname VARCHAR(255),
    verified_email VARCHAR(255),
    organisation_url VARCHAR(255),
    organisation_id VARCHAR(255),
    organisation_name VARCHAR(255),
    profile_image_url VARCHAR(255),
    profile_header_details VARCHAR(255),
    profile_header_details_links VARCHAR(255),
    citedby_total INT,
    h_index INT,
    i10_index INT,
    last5_citedby_total INT,
    last5_h_index INT,
    last5_i10_index INT,
    -- added from txt
    title VARCHAR(255),
    homepage_url VARCHAR(255),
    department_name VARCHAR(255),
    department_url VARCHAR(255)
);

CREATE TABLE coauthors (
    id INTEGER PRIMARY KEY,
    profile_level_attributes_id INT,
    google_scholar_id VARCHAR(255),
    fullname VARCHAR(255),
    organisation_name VARCHAR(255),
    profile_image_set VARCHAR(255),
    FOREIGN KEY (profile_level_attributes_id) REFERENCES profile_level_attributes(id)
);

CREATE TABLE publications (
    id INTEGER PRIMARY KEY,
    profile_level_attributes_id INT,
    google_scholar_id VARCHAR(255),
    publication_year INT,
    citedby_url VARCHAR(255),
    total_citations INT,
    publication_title VARCHAR(255),
    publication_url VARCHAR(255),
    publication_publish_url VARCHAR(255),
    publication_id VARCHAR(255),
    pdf_link VARCHAR(255),
    publication_type VARCHAR(255),
    issue VARCHAR(255),
    authors VARCHAR(255),
    publication_date VARCHAR(255),
    journal VARCHAR(255),
    pages VARCHAR(255),
    volume VARCHAR(255),
    conference VARCHAR(255),
    publisher VARCHAR(255),
    patent_office VARCHAR(255),
    book_name VARCHAR(255),
    citedby_total_url VARCHAR(255),
    pdf_text VARCHAR(255),
    description VARCHAR(255),
    source VARCHAR(255),
    FOREIGN KEY (profile_level_attributes_id) REFERENCES profile_level_attributes(id)
);

CREATE TABLE yearly_citations (
    id INTEGER PRIMARY KEY,
    publication_id INT,
    google_scholar_id INT
    citation_year INT,
    citation_count INT,
    FOREIGN KEY (publication_id) REFERENCES publications(publication_id),
    FOREIGN KEY (google_scholar_id) REFERENCES publications(google_scholar_id)
);
