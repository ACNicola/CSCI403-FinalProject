import getpass
import pg8000

try:
    # Username and password
    user = input("Username: ")
    secret = getpass.getpass()
    
    # Connect to the database
    db = pg8000.connect(user=user, password=secret, host='codd.mines.edu', port=5433, database='csci403')
    
    # Query execution
    query = """
    DROP TABLE IF EXISTS proportion_residental_robberies_RQ1 CASCADE;


-- -- "What Neigborhood(s) are associated with the highest proprtion for non-buisness related robberies"
CREATE TABLE proportion_residental_robberies_RQ1 AS
SELECT *
FROM full_crime_data
WHERE offense_type_id ILIKE 'burglary-residence-%' 
   OR offense_type_id ILIKE 'robbery-street-%' 
   OR offense_type_id ILIKE 'robbery-residence' 
   OR offense_type_id ILIKE 'burglary-other'
   AND neighborhood_id IS NOT NULL
   AND neighborhood_id != '';

( -- Top Burgaled Neigborhoods
    SELECT 
        neighborhood_id,
        COUNT(*) AS total_crimes
    FROM proportion_residental_robberies_RQ1
    GROUP BY neighborhood_id
    ORDER BY total_crimes DESC
    LIMIT 5
)
UNION ALL
( -- Bottom Burgaled Neighborhoods
    SELECT 
        neighborhood_id,
        COUNT(*) AS total_crimes
    FROM proportion_residental_robberies_RQ1
    GROUP BY neighborhood_id
    ORDER BY total_crimes ASC
    LIMIT 5
);

    """
    
    cursor = db.cursor()
    cursor.execute(query)
    
    # Fetch and print results
    results = cursor.fetchall()
    for row in results:
        print(row)
    
    # Clean up
    db.commit() # Finalize
    cursor.close()
    db.close()

except Exception as e:
    print(f"An error occurred: {e}")