CREATE TABLE contact (
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    location VARCHAR(255),
    github_link VARCHAR(255) CHECK (github_link LIKE 'https://github.com/%'), 
    linkedin_link VARCHAR(255) CHECK (linkedin_link LIKE 'https://linkedin.com/in/%'),
    professional_summary TEXT,
    PRIMARY KEY (first_name, last_name)
);

CREATE TABLE education (
    institution VARCHAR(255),
    degree VARCHAR(255),
    duration VARCHAR(19) CHECK (duration ~ '^[A-Za-z]{3} \d{4} - (?:[A-Za-z]{3} \d{4}|Present)$'), -- mmm yyyy - mmm yyyy or mmm yyyy - Present
    gpa VARCHAR(9) CHECK (gpa ~ '\d.\d{2}/4.00'), -- #.##/4.00
    PRIMARY KEY (institution, degree)
); 

CREATE TABLE employer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255), 
    location VARCHAR(255),
    UNIQUE (name, location)
); 

CREATE TABLE job (
    id SERIAL PRIMARY KEY,
    employer_id INTEGER,
    duration VARCHAR(19) CHECK (duration ~ '^[A-Za-z]{3} \d{4} - (?:[A-Za-z]{3} \d{4}|Present)$'), -- mmm yyyy - mmm yyyy or mmm yyyy - Present,
    title VARCHAR(255),
    FOREIGN KEY (employer_id) REFERENCES employer(id),
    UNIQUE (employer_id, title)

);

CREATE TABLE work_experience (
    id SERIAL PRIMARY KEY,
    job_id INTEGER, 
    job_description TEXT,
    FOREIGN KEY (job_id) REFERENCES job(id),
    UNIQUE (job_id, job_description)
);

CREATE TABLE skills (
    languages TEXT,
    technologies TEXT,
    PRIMARY KEY (languages, technologies)
); 

CREATE TABLE project (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(255), 
    code_repository VARCHAR(255) CHECK (code_repository LIKE 'https://%.%'),
    UNIQUE (name, code_repository)
); 

CREATE TABLE project_experience (
    id SERIAL PRIMARY KEY,
    project_id INTEGER,
    project_description TEXT,
    FOREIGN KEY (project_id) REFERENCES project(id),
    UNIQUE (project_id, project_description)
); 

CREATE TABLE certifying_org (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    UNIQUE (name)
); 

CREATE TABLE certification (
    org_id INTEGER,
    name VARCHAR(255) PRIMARY KEY,
    expiration_date CHAR(8) CHECK (expiration_date ~ '^[A-Za-z]{3} \d{4}$'), -- mmm yyyy
    FOREIGN KEY (org_id) REFERENCES certifying_org(id),
    UNIQUE (org_id, name)
); 