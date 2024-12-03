import getpass
import pg8000
# For splitting the .csv files of values into tables.
# Thomas Dowd
# Thomas McInnes
# Andrew Nicola
# Dmitry Weakly
# Hannah Clark
# try:
# Username and password
user = input("Username: ")
secret = getpass.getpass()

# Connect to the database
db = pg8000.connect(user=user, password=secret, host='codd.mines.edu', port=5433, database='csci403')
cursor = db.cursor()

# ~ ~ ~ IncidentTableCreation ~ ~ ~ #
query = """
    CREATE TABLE IF NOT EXISTS incident(
        objectid INT PRIMARY KEY, --make a primary (super?) key
        reported_date DATE,
        incident_address VARCHAR(255),
        is_traffic BOOLEAN,
        victim_count INT
        -- N:1 Relationship with Location
    );
"""
cursor.execute(query)

# ~ ~ ~ Geo-Location Table ~ ~ ~ #
query = '''
CREATE TABLE IF NOT EXISTS geo_location(
    id SERIAL PRIMARY KEY,
    geo_lon DOUBLE PRECISION,
    geo_lat DOUBLE PRECISION,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION
);
'''
cursor.execute(query)

# ~ ~ ~ LocationTableCreation ~ ~ ~ #
query = """
    CREATE TABLE IF NOT EXISTS location(    
        id INT PRIMARY KEY, -- Make Key
        geo_location_id INT, -- Reference to geo_location table
        district_id CHAR(1),
        precinct_id VARCHAR(50),
        neighborhood_id VARCHAR(50),
        FOREIGN KEY (geo_location_id) REFERENCES geo_location (id)
    );
"""
cursor.execute(query)

# Create occurrence_date Table
query = '''
CREATE TABLE IF NOT EXISTS occurrence_date(
    id SERIAL PRIMARY KEY,
    first_occurrence_date DATE,
    last_occurrence_date DATE
);
'''
cursor.execute(query)

# ~ ~ ~ OffenseTableCreation ~ ~ ~ #
query = '''
CREATE TABLE IF NOT EXISTS offense(
    offense_id DOUBLE PRECISION PRIMARY KEY, -- Make Key
    offense_code_extension VARCHAR(50),
    offense_type_id VARCHAR(50),
    offense_category_id VARCHAR(50),
    occurrence_date_id INT, -- Reference to occurrence_date table
    FOREIGN KEY (occurrence_date_id) REFERENCES occurrence_date (id)
);
'''
cursor.execute(query)




# Clean up
db.commit() # Finalize
cursor.close()
db.close()

# except Exception as e:
#     print(f"An error occurred: (e)")    