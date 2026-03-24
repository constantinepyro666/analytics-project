SELECT 
	--COUNT(DISTINCT CASE WHEN event_type = 'signup' THEN user_id END) as signup,
    --COUNT(DISTINCT CASE WHEN event_type = 'login' THEN user_id END) as login,
	--COUNT(DISTINCT CASE WHEN event_type = 'create_note' THEN user_id END) as create_note
	COUNT(DISTINCT user_id) AS users
FROM events
GROUP BY event_yype
ORDER BY users DASC
