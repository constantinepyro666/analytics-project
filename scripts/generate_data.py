import random
from datetime import datetime, timedelta
import pandas as pd

NUM_USERS = 1000
DAYS = 30

EVENTS = ["login", "view_note", "create_note"]

PLATFORMS = ["ios", "android", "web"]

def generate_users():
    users = []
    for user_id in range(1, NUM_USERS + 1):
        user_type = random.choices(
            ["active", "normal", "churn"],
            weights=[0.2, 0.5, 0.3]
        )[0]

        platform = random.choice(PLATFORMS)

        users.append({
            "user_id": user_id,
            "user_type": user_type,
            "platform": platform
        })

    return users


def generate_events(users):
    rows = []
    start_date = datetime.now() - timedelta(days=DAYS)

    for user in users:
        signup_date = start_date + timedelta(days=random.randint(0, 5))

        # signup событие
        rows.append({
            "user_id": user["user_id"],
            "event_type": "signup",
            "event_time": signup_date,
            "platform": user["platform"]
        })

        for day in range(DAYS):
            current_day = signup_date + timedelta(days=day)

            # вероятность возврата
            if user["user_type"] == "active":
                prob = 0.7
            elif user["user_type"] == "normal":
                prob = 0.4
            else:
                prob = 0.1

            if random.random() > prob:
                continue

            # login
            rows.append({
                "user_id": user["user_id"],
                "event_type": "login",
                "event_time": current_day,
                "platform": user["platform"]
            })

            # view_note
            if random.random() < 0.8:
                rows.append({
                    "user_id": user["user_id"],
                    "event_type": "view_note",
                    "event_time": current_day,
                    "platform": user["platform"]
                })

            # create_note
            if random.random() < 0.3:
                rows.append({
                    "user_id": user["user_id"],
                    "event_type": "create_note",
                    "event_time": current_day,
                    "platform": user["platform"]
                })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    users = generate_users()
    df = generate_events(users)

    df.to_csv("data/events.csv", index=False)

    print("Data generated:", len(df), "events")