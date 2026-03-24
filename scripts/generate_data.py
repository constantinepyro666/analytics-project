import pandas as pd
import random
from datetime import datetime, timedelta

NUM_USERS = 1000

events = []

start_date = datetime(2026, 2, 1)

for user_id in range(1, NUM_USERS + 1):
    # login (всегда)
    login_time = start_date + timedelta(days=random.randint(0, 30))
    events.append([user_id, "login", login_time, "web"])

    # 70% делают view_note
    if random.random() < 0.7:
        view_time = login_time + timedelta(minutes=random.randint(1, 60))
        events.append([user_id, "view_note", view_time, "web"])

        # 40% из них делают create_note
        if random.random() < 0.4:
            create_time = view_time + timedelta(minutes=random.randint(1, 60))
            events.append([user_id, "create_note", create_time, "web"])

df = pd.DataFrame(events, columns=["user_id", "event_type", "event_time", "platform"])

df.to_csv("events.csv", index=False)

print(f"Generated {len(df)} events")
