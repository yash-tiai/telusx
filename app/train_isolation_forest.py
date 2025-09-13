from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import joblib

# Load dataset
df = pd.read_csv("login_events_10k.csv")

# Feature engineering
df["login_hour"] = pd.to_datetime(df["login_time"]).dt.hour
df["geo_match"] = np.where((df["timezone"]=="IST") & (df["ip_country"]=="IN"), 1, 0)

# Device consistency = compare with most common device per user
main_devices = df.groupby("user_id")["device_hash"].agg(lambda x: x.value_counts().index[0])
df = df.merge(main_devices.rename("main_device"), on="user_id")
df["device_consistency"] = np.where(df["device_hash"] == df["main_device"], 1, 0)

# Encode categorical ISP
df["isp_type_enc"] = df["isp_type"].map({"residential": 1, "datacenter": 0})

# VPN flag to int
df["vpn_flag"] = df["vpn_flag"].astype(int)

# Final feature set
features = ["geo_match", "device_consistency", "login_hour", "isp_type_enc", "vpn_flag"]
X = df[features]
y = df["anomaly"]


# Train
model = IsolationForest(contamination=0.1, random_state=42, n_jobs=-1)
model.fit(X)

# Save the trained model
joblib.dump(model, "risk_engine_iforest.pkl")
print("Model saved as 'risk_engine_iforest.pkl'")

# Predict
df["pred"] = model.predict(X)   # 1 = normal, -1 = anomaly
df["pred"] = df["pred"].map({1:0, -1:1})  # map to anomaly=1

print(classification_report(y, df["pred"]))
