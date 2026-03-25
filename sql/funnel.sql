SELECT event_type, COUNT(DISTINCT user_id) as users
FROM events
GROUP BY event_type;
