import getpass
import pg8000
# For splitting the .csv files of values into tables.
# Thomas Dowd
# Thomas McInnes
# Andrew Nicola
# Dmitry Weakly
# Hannah Clark
try:
    # Username and password
    user = input("Username: ")
    secret = getpass.getpass()
    
    # Connect to the database
    db = pg8000.connect(user=user, password=secret, host='codd.mines.edu', port=5433, database='csci403')
    
    # ~ ~ ~ IncidentTableCreation ~ ~ ~ #
    query = """
        CREATE TABLE IF NOT EXISTS incident{
            objectid INT, --make a primary (super?) key
            reported_date DATE,
            incident_address VARCHAR(255),
            is_traffic BOOLEAN,
            victim_count INT
            -- N:1 Relationship with Location
        };
    """
    cursor = db.cursor()
    cursor.execute(query)
    
    # ~ ~ ~ LocationTableCreation ~ ~ ~ #
    query = """
        CREATE TABLE IF NOT EXISTS location{    
            geo_location TABLE, -- Make Key  (See Geo Location Table)     
            district_id CHAR(1),
            precinct_id VARCHAR(50),
            neighborhood_id VARCHAR(50),
        };
    """
    cursor = db.cursor()
    cursor.execute(query)
    # Create Geo-Location
    query = '''
    CREATE TABLE IF NOT EXISTS geo_location{
        geo_lon DOUBLE PRECISION,
        geo_lat DOUBLE PRECISION,
        x DOUBLE PRECISION,
        y DOUBLE PRECISION
    };
    '''
    cursor = db.cursor()
    cursor.execute(query)
    # ~ ~ ~ OffenseTableCreation ~ ~ ~ #
    query = '''
    CREATE TABLE IF NOT EXISTS offense{
        offense_id DOUBLE PRECISION, -- Make Key
        offense_code_extension VARCHAR(50),
        offense_type_id VARCHAR(50),
        offense_category_id VARCHAR(50),
        occurance_date TABLE -- Make Key (see occurance date table below)
    };
    '''
    cursor = db.cursor()
    cursor.execute(query)
    # Create occurance_date
    query = '''
    CREATE TABLE IF NOT EXISTS occurance_date{
        first_occurrence_date DATE,
        last_occurrence_date DATE
    };
    '''
    cursor = db.cursor()
    cursor.execute(query)
    
    
    # Clean up
    # db.commit() # Finalize
    cursor.close()
    db.close()

except Exception as e:
    print(f"An error occurred: {e}")    