#!/usr/bin/python3

import getpass
import pg8000

user = input("Username: ")
secret = getpass.getpass()
db = pg8000.connect(user=user, password=secret, host='codd.mines.edu', port=5433, database='csci403')

cursor = db.cursor()

# Delete Old tables (incident, full_crime_data) if they exist and add them to a new table
query = """

DROP TABLE IF EXISTS incident CASCADE;

CREATE TABLE IF NOT EXISTS full_crime_data (
    objectid INT,
    incident_id DOUBLE PRECISION,
    offense_id DOUBLE PRECISION,
    offense_code VARCHAR(50),
    offense_code_extension VARCHAR(50),
    offense_type_id VARCHAR(50),
    offense_category_id VARCHAR(50),
    first_occurrence_date DATE,
    last_occurrence_date DATE,
    reported_date DATE,
    incident_address VARCHAR(255),
    geo_x DOUBLE PRECISION,
    geo_y DOUBLE PRECISION,
    geo_lon DOUBLE PRECISION,
    geo_lat DOUBLE PRECISION,
    district_id CHAR(1),
    precinct_id VARCHAR(50),
    neighborhood_id VARCHAR(50),
    is_crime BOOLEAN,
    is_traffic BOOLEAN,
    victim_count INT,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION
);"""

cursor.execute(query)

# \COPY full_crime_data FROM 'C:\Users\<user>\Downloads\CLEANED_Denver_Crime.csv' (FORMAT csv, HEADER) in terminal

#Assume file is in project directory
db.commit()

cursor.close()
db.close()