from utils.mongo_client import get_mongo_db
from datetime import datetime, timezone

# 1. Get the MongoDB instance
db = get_mongo_db()

# 2. Amer's exact payload
payload = {
    "user_id": "S10",
    "timestamp": "2026-03-01T08:59:32.318Z",
    "features": {
      "hr_mean": 80.21,
      "hr_std": 0.2658,
      "hr_min": 79.93,
      "hr_max": 80.92,
      "hr_range": 0.9899,
      "eda_mean": 1.0064,
      "eda_std": 0.0153,
      "eda_min": 0.9853,
      "eda_max": 1.0313,
      "eda_range": 0.0460,
      "bvp_mean": 0.2615,
      "bvp_std": 18.1398,
      "bvp_min": -57.06,
      "bvp_max": 97.22,
      "bvp_range": 154.28,
      "ibi_mean": 0.7211,
      "ibi_std": 0.0923,
      "ibi_min": 0.5156,
      "ibi_max": 0.9219,
      "ibi_range": 0.4062,
      "acc_mag_mean": 62.8763,
      "acc_mag_std": 3.6469,
      "acc_mag_min": 36.3730,
      "acc_mag_max": 83.9344,
      "acc_mag_range": 47.5614,
      "ibi_rmssd": 0.0629,
      "acc_activity": 64.8992
    },
    "risk_level": "Low"
}

# 3. Add the server timestamp and insert
payload['server_received_at'] = datetime.now(timezone.utc)
result = db.risk_results.insert_one(payload)

print(f"\n--- SUCCESS! Document inserted with ID: {result.inserted_id} ---\n")