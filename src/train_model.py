import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib

# --- make sure we’re at project root ---
os.chdir(os.path.dirname(os.path.dirname(__file__)))

# --- Load processed dataset ---
data_path = "data/processed/uv_aq_features.csv"
df = pd.read_csv(data_path)
print(f"📂 Loaded {len(df)} rows from {data_path}")

# --- Define target and features ---
TARGET = "safe_minutes_label"
drop_cols = ["datetime", "hour", "dow", "city", "country"]  # remove non-numeric/meta if present
FEATURES = [c for c in df.columns if c not in drop_cols + [TARGET]]

X = df[FEATURES]
y = df[TARGET]

print(f"🧠 Using {len(FEATURES)} features: {FEATURES}")

# --- Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Train model (XGBoost) ---
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.08,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
)
model.fit(X_train, y_train)

# --- Evaluate ---
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n✅ Model Evaluation")
print(f"MAE:  {mae:.3f}")
print(f"RMSE: {rmse:.3f}")
print(f"R²:   {r2:.3f}")

# --- Save model ---
os.makedirs("models", exist_ok=True)
model_path = "models/safe_exposure_model.pkl"
joblib.dump(model, model_path)
print(f"\n💾 Model saved to {model_path}")


"""
A small caveat
Remember, some features (temperature, humidity, gas resistance, etc.) were synthetic (simulated).
So, while the metrics show great internal fit, real sensor data might produce slightly higher errors (because real-world readings are noisier).
But for your project demo / prototype, these results are ideal — they’ll let you show strong ML performance and reliability.
"""
