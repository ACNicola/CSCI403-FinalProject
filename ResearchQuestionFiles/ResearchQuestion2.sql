
-- @Author Andrew
-- @Author Thomas
SELECT offense_type_id, COUNT(offense_type_id) * 1.0 / (SELECT COUNT(*) FROM full_crime_data) 
    AS proportion 
    FROM full_crime_data 
    GROUP BY offense_type_id 
    ORDER BY proportion DESC
    limit 15;