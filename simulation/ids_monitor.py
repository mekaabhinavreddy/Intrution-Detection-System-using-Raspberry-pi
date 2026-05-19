import pandas as pd
import joblib
import time

model    = joblib.load("models/ids_model.pkl")
scaler   = joblib.load("models/scaler.pkl")
selector = joblib.load("models/selector.pkl")

df = pd.read_csv("simulation/live_traffic.csv")

print("=== IDS Monitor Started ===")
print()

normal_count = 0
alert_count  = 0

for _, row in df.iterrows():
    features = row.values.reshape(1, -1)
    pred     = model.predict(features)[0]

    if pred == "normal":
        normal_count += 1
        print(f"[OK]    Normal traffic")
    else:
        alert_count += 1
        print(f"[ALERT] {pred.upper()} attack detected!")

    time.sleep(0.05)

print()
print("=== Summary ===")
print(f"Total packets : {len(df)}")
print(f"Normal        : {normal_count}")
print(f"Attacks caught: {alert_count}")