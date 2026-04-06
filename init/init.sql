-- создаём таблицу
CREATE TABLE events (
    user_id INT,
    event_type TEXT,
    event_time TIMESTAMP,
    platform TEXT
);

-- загружаем данные
COPY events(user_id, event_type, event_time, platform)
FROM '/docker-entrypoint-initdb.d/events.csv'
DELIMITER ','
CSV HEADER;
