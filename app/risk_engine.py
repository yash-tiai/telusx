# ============================
# 1. Import Libraries
# ============================
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_login_anomalies(login_data, base_country="IN", base_timezone="IST", contamination=0.3, random_state=42):
    """
    Detect anomalous login attempts using Isolation Forest algorithm.
    
    Args:
        login_data (list): List of dictionaries containing login information
        base_country (str): Expected country code for the base timezone (default: "IN")
        base_timezone (str): Base timezone to compare against (default: "IST")
        contamination (float): Expected proportion of anomalies (default: 0.3)
        random_state (int): Random state for reproducibility (default: 42)
    
    Returns:
        pandas.DataFrame: DataFrame with original data plus anomaly scores and predictions
    """
    
    # ============================
    # 2. Convert Data to DataFrame
    # ============================
    df = pd.DataFrame(login_data)
    
    # Ensure vpn_flag is boolean
    if 'vpn_flag' in df.columns:
        df['vpn_flag'] = df['vpn_flag'].astype(bool)
    
    print(f"Processing {len(df)} login records...")
    print(f"Base country: {base_country}, Base timezone: {base_timezone}")
    # ============================
    # 3. Feature Engineering
    # ============================
    
    # Extract login hour
    df["login_hour"] = pd.to_datetime(df["login_time"]).dt.hour
    
    # Geo match (ip_country == base_country when timezone == base_timezone)
    df["geo_match"] = np.where(
        (df["timezone"] == base_timezone) & (df["ip_country"] == base_country), 1, 0
    )
    
    # Device consistency: compare with first seen device for each user
    df["device_consistency"] = 0
    for user_id in df["user_id"].unique():
        user_mask = df["user_id"] == user_id
        if user_mask.sum() > 0:
            main_device = df[user_mask]["device_hash"].iloc[0]
            df.loc[user_mask, "device_consistency"] = np.where(
                df.loc[user_mask, "device_hash"] == main_device, 1, 0
            )
    
    # Encode categorical ISP type
    df["isp_type_enc"] = df["isp_type"].map({"residential": 1, "datacenter": 0})
    
    # VPN flag to int
    df["vpn_flag"] = df["vpn_flag"].astype(int)
    
    # Final feature set
    features = ["geo_match", "device_consistency", "login_hour", "isp_type_enc", "vpn_flag"]
    X = df[features]
    
    print("Feature Data:\n", X)
    
    # ============================
    # 4. Train Isolation Forest
    # ============================
    model = IsolationForest(contamination=contamination, random_state=random_state)
    model.fit(X)
    
    df["anomaly_score"] = model.decision_function(X)
    df["is_anomaly"] = model.predict(X)  # -1 = anomaly, 1 = normal
    
    # Convert to readable format
    df["is_anomaly"] = df["is_anomaly"].map({1: "Normal", -1: "Anomaly"})
    
    return df

# # ============================
# # 5. Example Usage
# # ============================
# if __name__ == "__main__":
#     # Sample login data
#     sample_data = [
#         # Normal logins (India, same device, no VPN)
#         {"user_id": "u123", "login_time": "2025-09-12 10:30:00", "ip_country": "IN", "timezone": "IST", "device_hash": "A1B2C3", "isp_type": "residential", "vpn_flag": False},
#         {"user_id": "u123", "login_time": "2025-09-12 14:15:00", "ip_country": "IN", "timezone": "IST", "device_hash": "A1B2C3", "isp_type": "residential", "vpn_flag": False},
#         {"user_id": "u123", "login_time": "2025-09-12 09:05:00", "ip_country": "IN", "timezone": "IST", "device_hash": "A1B2C3", "isp_type": "residential", "vpn_flag": False},
#         {"user_id": "u123", "login_time": "2025-09-12 09:05:00", "ip_country": "AU", "timezone": "IST", "device_hash": "A1B2C3", "isp_type": "residential", "vpn_flag": False},
#         {"user_id": "u1234", "login_time": "2025-09-12 10:30:00", "ip_country": "IN", "timezone": "IST", "device_hash": "A1B2C3", "isp_type": "residential", "vpn_flag": False},
#
#         # Suspicious logins (different country, VPN, new device, odd hour)
#         {"user_id": "u123", "login_time": "2025-09-12 02:00:00", "ip_country": "RU", "timezone": "IST", "device_hash": "Z9Y8X7", "isp_type": "datacenter", "vpn_flag": True},
#         {"user_id": "u123", "login_time": "2025-09-12 03:30:00", "ip_country": "US", "timezone": "IST", "device_hash": "P9Q8W7", "isp_type": "datacenter", "vpn_flag": True}
#     ]
#
#     # Run anomaly detection with default base country and timezone
#     results = detect_login_anomalies(sample_data)
#
#     # Example with custom base country and timezone
#     # results = detect_login_anomalies(sample_data, base_country="US", base_timezone="EST")
#
#     # Show results
#     print("\nResults:")
#     print(results[["user_id", "login_time", "ip_country", "device_hash", "anomaly_score", "is_anomaly"]])
