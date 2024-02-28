CREATE TABLE client_informations (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    short_name TEXT,
    department_name TEXT,
    department_short_name TEXT,
    status TEXT NOT NULL DEFAULT 'new',
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    client_data_sheet_link TEXT,
    department_subscribed BOOLEAN DEFAULT 0,
    applicant_subscribed BOOLEAN DEFAULT 0,
    journal_subscribed BOOLEAN DEFAULT 0,
    department_data_last_update DATETIME,
    applicant_data_last_update DATETIME,
    journal_data_last_update DATETIME,
    data_update_period TEXT
);
