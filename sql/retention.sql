WITH first_visit AS (
SELECT 
user_id, 
MIN(DATE(event_time)) AS first_date 
FROM events
GROUP BY user_id
ORDER BY first_date
),
activity AS (
SELECT
e.user_id,
DATE(e.event_time) AS event_time,
f.first_date,
DATE(e.event_time) - f.first_date AS day
FROM events e
JOIN first_visit f ON e.user_id = f.user_id
),

cohort_size AS (SELECT COUNT(DISTINCT user_id) as total_users FROM first_visit)

SELECT
day,
COUNT(DISTINCT user_id) AS users,
ROUND(COUNT(DISTINCT user_id)*100 / (SELECT total_users FROM cohort_size), 2) AS retention_percent
FROM
activity
GROUP BY day
ORDER BY day
LIMIT 15