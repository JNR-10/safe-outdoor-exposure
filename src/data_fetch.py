import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
CITIES = [c.strip() for c in os.getenv("CITIES", "San Jose").split(",")]
COUNTRY = os.getenv("COUNTRY", "US")
DAYS = int(os.getenv("DAYS", 30))

# --- Date range ---
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=DAYS)
print(f"📅 Fetching data from {start_date} to {end_date}")

# --- Output storage ---
records = []

for CITY in CITIES:
    print(f"\n📍 Fetching data for {CITY}")

    # --- Get coordinates via Nominatim ---
    geo_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": CITY + ", " + COUNTRY, "format": "json", "limit": 1}
    headers = {"User-Agent": "IoT-Project-DataFetch/1.0 (edu use)"}

    try:
        geo_resp = requests.get(geo_url, params=params, headers=headers, timeout=15).json()
    except Exception as e:
        print(f"⚠️ Geocoding failed for {CITY}: {e}")
        continue

    if not geo_resp:
        print(f"⚠️ Skipping {CITY} — no coordinates found.")
        continue

    lat, lon = float(geo_resp[0]["lat"]), float(geo_resp[0]["lon"])
    print(f"   Coordinates: lat={lat:.3f}, lon={lon:.3f}")

    # --- UV data from Open-Meteo ---
    uv_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=uv_index&timezone=auto"
        f"&start_date={start_date}&end_date={end_date}"
    )
    uv_json = requests.get(uv_url, timeout=20).json()
    if "hourly" not in uv_json:
        print(f"⚠️ No UV data for {CITY}.")
        continue

    uv_df = pd.DataFrame({
        "datetime": pd.to_datetime(uv_json["hourly"]["time"]),
        "uv_index": uv_json["hourly"]["uv_index"]
    })

    # --- AQI / PM2.5 from AirNow (historical lat/long endpoint) ---
    AIRNOW_KEY = os.getenv("AIRNOW_KEY")
    if not AIRNOW_KEY:
        raise ValueError("❌ AIRNOW_KEY not found in .env file!")

    aq_frames = []
    for day_offset in range(DAYS):
        day = end_date - timedelta(days=day_offset)
        aq_url = (
            f"http://www.airnowapi.org/aq/observation/latLong/historical/"
            f"?format=application/json"
            f"&latitude={lat}&longitude={lon}"
            f"&date={day.strftime('%Y-%m-%dT00-0000')}"
            f"&distance=100"  # increased radius for denser data
            f"&API_KEY={AIRNOW_KEY}"
        )

        try:
            resp = requests.get(aq_url, timeout=20)
            resp.raise_for_status()
            daily_json = resp.json()
            if daily_json:
                aq_frames.append(pd.DataFrame(daily_json))
                print(f"✅ AirNow {CITY}: {len(daily_json)} records for {day}")
        except Exception as e:
            print(f"⚠️ AirNow request failed for {CITY} ({day}): {e}")

    # --- Combine daily PM2.5 frames ---
    if not aq_frames:
        print(f"⚠️ No AirNow PM2.5 data for {CITY} — using synthetic fallback.")
        aq_df = pd.DataFrame({
            "datetime": uv_df["datetime"],
            "pm25": [None] * len(uv_df)
        })
    else:
        aq_df = pd.concat(aq_frames, ignore_index=True)
        # Detect columns dynamically
        value_col = next((c for c in ["Value", "PM2.5", "PM25", "Concentration", "AQI"] if c in aq_df.columns), None)
        time_col = next((c for c in ["DateObserved", "UTC", "DateTime"] if c in aq_df.columns), None)

        if not value_col or not time_col:
            print(f"⚠️ Could not find PM2.5 or time columns for {CITY}. Columns: {aq_df.columns.tolist()}")
            aq_df = pd.DataFrame({
                "datetime": uv_df["datetime"],
                "pm25": [None] * len(uv_df)
            })
        else:
            aq_df["datetime"] = pd.to_datetime(aq_df[time_col], errors="coerce")
            aq_df = aq_df.rename(columns={value_col: "pm25"})
            aq_df = aq_df[["datetime", "pm25"]].dropna(subset=["datetime", "pm25"])
            print(f"✅ Combined {len(aq_df)} PM2.5 records for {CITY} from AirNow.")

    # --- Merge UV + PM ---
    uv_df["datetime"] = pd.to_datetime(uv_df["datetime"], errors="coerce")
    aq_df["datetime"] = pd.to_datetime(aq_df["datetime"], errors="coerce")

    merged = pd.merge_asof(
        uv_df.sort_values("datetime"),
        aq_df.sort_values("datetime"),
        on="datetime",
        direction="nearest",
        tolerance=pd.Timedelta("1h"),
    )

    merged["city"] = CITY
    merged["country"] = COUNTRY
    records.append(merged)

# --- Combine all cities ---
if not records:
    raise ValueError("No data fetched for any city.")

df_all = pd.concat(records, ignore_index=True).dropna(subset=["uv_index"]).reset_index(drop=True)

# --- Save dataset ---
os.makedirs("data/raw", exist_ok=True)
out_path = "data/raw/merged_uv_aq_multi.csv"
df_all.to_csv(out_path, index=False)
print(f"\n✅ Combined dataset saved to {out_path}")
print(f"Total rows: {len(df_all)}")
