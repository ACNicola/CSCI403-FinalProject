
-- @Author Andrew
SELECT offense_type_id, COUNT(offense_type_id) * 1.0 / (SELECT COUNT(*) FROM incident) 
    AS proportion 
    FROM incident 
    GROUP BY offense_type_id 
    ORDER BY proportion DESC
    limit 15;