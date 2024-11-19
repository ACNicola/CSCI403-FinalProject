
-- Get into PSQL Terminal + All preprossing seen above
-- If your'e runing from beginning:
DROP TABLE IF EXISTS relevant_crimes_rq1 CASCADE;
-- Create Table 

-- "What Neigborhood(s) are associated with the highest proprtion for non-buisness related robberies"
CREATE TABLE relevant_crimes_rq1 AS
SELECT *
FROM incident
WHERE offense_type_id ILIKE 'burglary-residence-%' 
   OR offense_type_id ILIKE 'robbery-street-%' 
   OR offense_type_id ILIKE 'robbery-residence' 
   OR offense_type_id ILIKE 'burglary-other'
   AND neighborhood_id IS NOT NULL
   AND neighborhood_id != '';

-- 

SELECT neighborhood_id, incident_address, offense_type_id
FROM relevant_crimes_rq1
LIMIT 10;

-- Select Statement to grab the neigborhoods that have been found to have the most crime
-- TODO: Fix the problem with a no-name 

( -- Top Burgaled Neigborhoods
    SELECT 
        neighborhood_id,
        COUNT(*) AS total_crimes
    FROM relevant_crimes_rq1
    GROUP BY neighborhood_id
    ORDER BY total_crimes DESC
    LIMIT 5
);

( -- Bottom Burgaled Neighborhoods
    SELECT 
        neighborhood_id,
        COUNT(*) AS total_crimes
    FROM relevant_crimes_rq1
    GROUP BY neighborhood_id
    ORDER BY total_crimes ASC
    LIMIT 5
);


