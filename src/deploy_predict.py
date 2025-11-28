import os
import time
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from math import sin, cos, pi
from random import uniform  # replace with sensor readings later

# --- always start at project root ---
os.chdir(os.path.dirname(os.path.dirname(__file__)))

# Load trained model
model_path = "models/safe_exposure_model.pkl"
model = joblib.load(model_path)
print(f"✅ Model loaded from {model_path}")

# --- helper functions ---
def compute_features(uv_index, pm25, temp_c, hum_rh, press_hpa, gas_res_ohm, lux):
    dew_c = temp_c - ((100 - hum_rh) / 5)
    hi = (
        -8.784695 + 1.61139411*temp_c + 2.338549*hum_rh - 0.14611605*temp_c*hum_rh
        - 0.012308094*temp_c**2 - 0.016424828*hum_rh**2
        + 0.002211732*temp_c**2*hum_rh + 0.00072546*temp_c*hum_rh**2
        - 0.000003582*temp_c**2*hum_rh**2
    )
    uv_vis_ratio = (uv_index + 1e-6) / (lux + 1e-6)

    now = datetime.now()
    hour = now.hour + now.minute / 60
    dow = now.weekday()

    hour_sin = sin(2 * pi * hour / 24)
    hour_cos = cos(2 * pi * hour / 24)
    dow_sin = sin(2 * pi * dow / 7)
    dow_cos = cos(2 * pi * dow / 7)

    return pd.DataFrame([{
        "uv_index": uv_index,
        "pm25": pm25,
        "temp_c": temp_c,
        "hum_rh": hum_rh,
        "press_hpa": press_hpa,
        "gas_res_ohm": gas_res_ohm,
        "lux": lux,
        "dew_c": dew_c,
        "heat_index": hi,
        "uv_vis_ratio": uv_vis_ratio,
        "hour_sin": hour_sin,
        "hour_cos": hour_cos,
        "dow_sin": dow_sin,
        "dow_cos": dow_cos
    }])

# --- Live loop (simulate sensors now) ---
print("\n Starting live prediction loop (Ctrl+C to stop)...\n")

while True:
    # replace the random values below with actual sensor readings
    uv_index = uniform(0, 10)
    pm25 = uniform(10, 80)
    temp_c = uniform(15, 35)
    hum_rh = uniform(30, 80)
    press_hpa = uniform(1008, 1016)
    gas_res_ohm = uniform(10_000, 1_000_000)
    lux = uv_index * 10_000 + uniform(100, 300)

    features = compute_features(uv_index, pm25, temp_c, hum_rh, press_hpa, gas_res_ohm, lux)
    prediction = model.predict(features)[0]

    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
          f"Sensor_Aggregation={uv_index:.2f}, AQI≈{pm25:.1f}, Temp={temp_c:.1f}°C → "
          f"Safe Exposure ≈ {prediction:.1f} min")

    time.sleep(3)  # every 3 seconds
