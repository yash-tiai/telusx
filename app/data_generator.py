import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ============================
# 1. Parameters
# ============================
NUM_USERS = 10000
EVENTS_PER_USER = 5   # avg login events per user
ANOMALY_USERS = 500   # users who will have anomalies
random.seed(42)
np.random.seed(42)

# ============================
# 2. Helper Functions
# ============================
def random_time():
    """Generate a random login timestamp within last 30 days"""
    base = datetime.now() - timedelta(days=np.random.randint(0, 30))
    return base.replace(hour=np.random.randint(8, 22), minute=np.random.randint(0, 60))

def generate_device_hash():
    return ''.join(random.choices("ABCDEF1234567890", k=6))

def generate_normal_event(user_id, device_hash):
    return {
        "user_id": user_id,
        "login_time": random_time(),
        "ip_country": "IN",
        "timezone": "IST",
        "device_hash": device_hash,
        "isp_type": "residential",
        "vpn_flag": False,
        "anomaly": 0
    }

def generate_anomaly_event(user_id):
    countries = ["RU", "US", "CN", "BR", "DE"]
    timezones = ["IST", "EST", "UTC", "CST"]
    return {
        "user_id": user_id,
        "login_time": datetime.now().replace(hour=np.random.randint(0, 6), minute=np.random.randint(0, 60)),
        "ip_country": random.choice(countries),
        "timezone": random.choice(timezones),
        "device_hash": generate_device_hash(),
        "isp_type": "datacenter",
        "vpn_flag": True,
        "anomaly": 1
    }

# ============================
# 3. Data Generation
# ============================
data = []
all_users = [f"user_{i}" for i in range(1, NUM_USERS+1)]
anomaly_users = set(random.sample(all_users, ANOMALY_USERS))

for user in all_users:
    main_device = generate_device_hash()
    for _ in range(EVENTS_PER_USER):
        if user in anomaly_users and np.random.rand() < 0.3:  # 30% of events anomalous
            data.append(generate_anomaly_event(user))
        else:
            data.append(generate_normal_event(user, main_device))

# ============================
# 4. Create DataFrame
# ============================
df = pd.DataFrame(data)

print("Dataset shape:", df.shape)
print(df.head())

# Save CSV for later use
df.to_csv("login_events_10k.csv", index=False)
