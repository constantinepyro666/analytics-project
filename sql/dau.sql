SELECT 
    DATE(event_time) as date,
    platform,
    COUNT(DISTINCT user_id) as dau
FROM user_events
GROUP BY date, platform
