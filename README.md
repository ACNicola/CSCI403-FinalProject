Prior: Download Data, have python/psql installed


First: Preprocess Data (some rows were exported without all columns, creates CSVs for SQL table creation)

`preprocess.py`
```
import csv

input_file = "Denver_Crime.csv" 			# Whatever your file name actually is
output_file = "CLEANED_Denver_Crime.csv"		# What you want your new file name to be (cannot be the same as input_file)
N_COLUMNS = 23 						# There are 23 columns in the .csv

with open(input_file, 'r') as input, open(output_file, 'w', newline='') as output:
  reader = csv.reader(input)
  writer = csv.writer(output)

  for row in reader:
    while len(row) < N_COLUMNS:
      row.append('')

    writer.writerow(row)

with open("CLEANED_Denver_Crime.csv", 'r') as input, open("incident.csv", 'w', newline='') as incident, open("offense.csv", 'w', newline='') as offense, open("location.csv", 'w', newline='') as location:
  reader = csv.reader(input)
  inciWriter = csv.writer(incident)
  offWriter = csv.writer(offense)
  locWriter = csv.writer(location)

  for row in reader:
    idx = 0
    incidentRow = []
    offenseRow = []
    locationRow = []
    for col in row:
      if idx in INCIDENT_COLS:
        incidentRow.append(col)
      elif idx in OFFENSE_COLS:
        offenseRow.append(col)
      elif idx in LOCATION_COLS:
        locationRow.append(col)
      idx += 1
    inciWriter.writerow(incidentRow)
    offWriter.writerow(offenseRow)
    locWriter.writerow(locationRow)
```

Run `preprocess.py` in the same directory as your data download (or change input_file to include the path)
Should create 4 .csv files: CLEANED_Denver_Crime, incident, offense, location

Second: Create Tables

```
CREATE TABLE full_crime_data (
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
);
CREATE TABLE incident (
    incident_id DOUBLE PRECISION,
    reported_date DATE,
    incident_address VARCHAR(255),
    is_traffic BOOLEAN,
    victim_count INT
);
CREATE TABLE offense (
    offense_id DOUBLE PRECISION,
    offense_code VARCHAR(50),
    offense_code_extension VARCHAR(50),
    offense_type_id VARCHAR(50),
    offense_category_id VARCHAR(50),
    first_occurrence_date DATE,
    last_occurrence_date DATE
);
CREATE TABLE location (
    geo_lon DOUBLE PRECISION,
    geo_lat DOUBLE PRECISION,
    district_id CHAR(1),
    precinct_id VARCHAR(50),
    neighborhood_id VARCHAR(50),
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    location_id SERIAL
);
```
* Not all columns are minimized, but this works to get it all loaded
* geo_x and geo_y seem to be empty, while x and y seem to actually hold the values we expect (I'm too lazy to change that right now)

Third: Load Data

```			
Sub your drive, <user>, path, and file name to this
\COPY full_crime_data FROM 'C:\Users\<user>\Downloads\CLEANED_Denver_Crime.csv' (FORMAT csv, HEADER)
\COPY incident FROM 'C:\Users\<user>\Downloads\incident.csv' (FORMAT csv, HEADER)
\COPY offense FROM 'C:\Users\<user>\Downloads\offense.csv' (FORMAT csv, HEADER)
\COPY location FROM 'C:\Users\<user>\Downloads\location.csv' (FORMAT csv, HEADER)
```

You should see ouput: `COPY 396535` for the full_crime_data table.

Further verify it worked by running `\d full_crime_data` and `SELECT TOP 10 * FROM full_crime_data;`
Test to ensure the SERIAL type works for location by running `\d location` and `SELECT TOP 10 * FROM location`
