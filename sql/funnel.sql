SELECT 
    platform,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'login') as login,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'view_note') as view_note,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'create_note') as create_note
FROM user_events
GROUP BY platform;
