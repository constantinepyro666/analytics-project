SELECT
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'login') AS login,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'view_note') AS view_note,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'create_note') AS create_note
FROM events;
