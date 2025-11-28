import os
import joblib
import streamlit as st
from datetime import datetime
from src.deploy_predict import compute_features

st.set_page_config(page_title="☀️ Adaptive UV & AQI Dashboard", page_icon="☀️", layout="wide")

# simple visible text so we know it renders
st.title("☀️ Adaptive UV & Air Quality Co-Optimization Dashboard")
st.write("If you see this text, Streamlit is rendering correctly ✅")

# ---- load model ----
model_path = "models/safe_exposure_model.pkl"
if not os.path.exists(model_path):
    st.error("⚠️ Trained model not found! Please run `train_model.py` first.")
    st.stop()
model = joblib.load(model_path)

# ---- simple sliders ----
uv = st.slider("UV Index", 0.0, 11.0, 5.0)
pm25 = st.slider("PM2.5 (µg/m³)", 0.0, 200.0, 60.0)
temp = st.slider("Temperature (°C)", 10.0, 45.0, 28.0)
hum = st.slider("Humidity (%)", 10.0, 100.0, 50.0)
press = st.slider("Pressure (hPa)", 1000.0, 1020.0, 1013.0)
gas = st.slider("Gas Resistance (Ω)", 1e4, 1e6, 5e5)
lux = st.slider("Visible Light (lux)", 0.0, 100000.0, 30000.0)

# ---- compute features & predict ----
features = compute_features(uv, pm25, temp, hum, press, gas, lux)
prediction = model.predict(features)[0]

# ---- main output ----
st.subheader("Predicted Safe Exposure Time")
st.metric("Safe Outdoor Exposure", f"{prediction:.1f} minutes")
st.caption(f"Updated {datetime.now():%Y-%m-%d %H:%M:%S}")

with st.expander("See computed features"):
    st.dataframe(features)
