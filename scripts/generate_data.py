import pandas as pd
import random
from datetime import datetime, timedelta
import os
os.makedirs("data", exist_ok=True)

NUM_USERS = 1000

events = []

start_date = datetime(2026, 2, 1)

for user_id in range(1, NUM_USERS + 1):
    # login (всегда)
    login_time = start_date + timedelta(days=random.randint(0, 30))
    events.append([user_id, "login", login_time, "web"])

    # view_note
    if random.random() < 0.7:
        view_time = login_time + timedelta(days=random.randint(0, 5))
        events.append([user_id, "view_note", view_time, "web"])

    # create_note
    if random.random() < 0.4:
        create_time = login_time + timedelta(days=random.randint(0, 5))
        events.append([user_id, "create_note", create_time, "web"])

df = pd.DataFrame(events, columns=["user_id", "event_type", "event_time", "platform"])

df.to_csv("data/events.csv", index=False)

print(f"Generated {len(df)} events")
