SELECT 
	--CAST (event_time AS date) as dau,
	DATE(event_time) AS date,
	COUNT(distinct user_id) as dau
FROM events
GROUP BY date
ORDER BY date