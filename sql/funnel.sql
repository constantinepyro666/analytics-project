--SELECT event_type, COUNT(DISTINCT user_id) as users
--FROM events
--GROUP BY event_type;
SELECT event_type, COUNT(DISTINCT user_id) AS users
FROM events
GROUP BY event_type
ORDER BY 
    CASE event_type
        WHEN 'login' THEN 1
        WHEN 'view_note' THEN 2
        WHEN 'create_note' THEN 3
    END;
