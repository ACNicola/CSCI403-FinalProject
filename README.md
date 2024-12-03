Prior: Download Data, have python/psql installed


First: Preprocess Data (some rows were exported without all columns)

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
```

Run `preprocess.py` in the same directory as your data download (or change input_file to include the path)


Second: Create Table

```
CREATE TABLE incident (
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
```
* Not all columns are minimized, but this works to get it all loaded
* geo_x and geo_y seem to be empty, while x and y seem to actually hold the values we expect (I'm too lazy to change that right now)

Third: Load Data

```			
Sub your drive, <user>, path, and file name to this
\COPY incident FROM 'C:\Users\<user>\Downloads\CLEANED_Denver_Crime.csv' (FORMAT csv, HEADER)
```

You should see an ouput: `COPY 396535`

Further verify it worked by running `\d incident` and `SELECT TOP 10 * FROM incident;`