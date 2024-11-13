#!/usr/bin/python3

import getpass
import pg8000
import csv

user = input("Username: ")
secret = getpass.getpass()
db = pg8000.connect(user=user, password=secret, host='codd.mines.edu', port=5433, database='csci403')

cursor = db.cursor()

query = """CREATE TABLE incident (
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

with open('./CLEANED_Denver_Crime.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    query = """
    INSERT INTO incident (
        objectid, incident_id, offense_id, offense_code, offense_code_extension, offense_type_id,
        offense_category_id, first_occurrence_date, last_occurrence_date, reported_date, 
        incident_address, geo_x, geo_y, geo_lon, geo_lat, district_id, precinct_id, 
        neighborhood_id, is_crime, is_traffic, victim_count, x, y
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    for row in reader:
        row = [None if col == "" else col for col in row]
        cursor.execute(query, row)

#Assume file is in project directory
db.commit()

cursor.close()
db.close()