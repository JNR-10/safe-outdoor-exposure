import os
import numpy as np
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- Ensure correct working directory ---
os.chdir(os.path.dirname(os.path.dirname(__file__)))

# --- Load dataset ---
in_path = "data/raw/merged_uv_aq_multi.csv"
df = pd.read_csv(in_path)
print(f"📂 Loaded {len(df)} rows from {in_path}")

# --- Convert datetime ---
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
df = df.dropna(subset=["datetime"]).reset_index(drop=True)

# --- Fill or simulate missing environmental features ---
np.random.seed(42)
hours = df["datetime"].dt.hour

# Temperature, humidity, pressure — synthetic until sensors connected
df["temp_c"] = 15 + 10 * np.sin((hours - 6) * np.pi / 12) + np.random.normal(0, 1, len(df))
df["hum_rh"] = 60 - 20 * np.sin((hours - 6) * np.pi / 12) + np.random.normal(0, 3, len(df))
df["press_hpa"] = 1013 + np.random.normal(0, 1, len(df))
df["gas_res_ohm"] = np.random.uniform(10_000, 1_000_000, len(df))
df["lux"] = (df["uv_index"] * 10_000) + np.random.normal(500, 200, len(df))
df["lux"] = df["lux"].clip(lower=0)

# Fill missing PM2.5 values if any
df["pm25"] = df["pm25"].fillna(df["pm25"].mean())

# --- Derived features ---
df["dew_c"] = df["temp_c"] - ((100 - df["hum_rh"]) / 5)
T, RH = df["temp_c"], df["hum_rh"]
df["heat_index"] = (
    -8.784695 + 1.61139411*T + 2.338549*RH - 0.14611605*T*RH
    - 0.012308094*T**2 - 0.016424828*RH**2
    + 0.002211732*T**2*RH + 0.00072546*T*RH**2
    - 0.000003582*T**2*RH**2
)
df["uv_vis_ratio"] = (df["uv_index"] + 1e-6) / (df["lux"] + 1e-6)

# Time-based features
df["hour"] = df["datetime"].dt.hour + df["datetime"].dt.minute / 60
df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
df["dow"] = df["datetime"].dt.dayofweek
df["dow_sin"] = np.sin(2 * np.pi * df["dow"] / 7)
df["dow_cos"] = np.cos(2 * np.pi * df["dow"] / 7)

# --- Safe exposure rule ---
def base_minutes_from_uvi(uvi):
    if uvi < 3: return 60
    if uvi < 6: return 30
    if uvi < 8: return 20
    if uvi < 11: return 10
    return 5

def aqi_multiplier(pm25):
    if pm25 <= 50: return 1.0
    if pm25 <= 100: return 0.8
    if pm25 <= 150: return 0.6
    if pm25 <= 200: return 0.4
    return 0.25

def heat_adj(hi):
    if hi >= 38: return 0.6
    if hi >= 32: return 0.8
    return 1.0

df["safe_minutes_label"] = [
    max(1, round(base_minutes_from_uvi(u) * aqi_multiplier(p) * heat_adj(h), 1))
    for u, p, h in zip(df["uv_index"], df["pm25"], df["heat_index"])
]

# --- Save processed dataset ---
os.makedirs("data/processed", exist_ok=True)
out_path = "data/processed/uv_aq_features.csv"
df.to_csv(out_path, index=False)
print(f"✅ Processed dataset saved to {out_path}")
print(f"Columns: {df.columns.tolist()}")
print(df.head(10))
