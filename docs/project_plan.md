# 📅 Project Plan: Adaptive UV & Air Quality System

## 🎯 Project Goal
To build an IoT-enabled system that aggregates environmental data (UV, Air Quality, Weather) and uses Machine Learning to recommend safe outdoor exposure durations, promoting better public health decisions.

## 🗓️ Phases

### Phase 1: Design & Architecture (✅ Completed)
*   [x] Define system requirements and use cases.
*   [x] Design software architecture (Data Pipeline, ML Model, UI).
*   [x] Select technology stack (Python, Streamlit, XGBoost).
*   [x] Create architecture diagrams.

### Phase 2: Data Engineering (✅ Completed)
*   [x] Implement `data_fetch.py` to interface with Open-Meteo and AirNow APIs.
*   [x] Implement geocoding for multi-city support.
*   [x] Create data merging logic (UV + Air Quality + Weather).
*   [x] Automate CSV dataset generation.

### Phase 3: Machine Learning (✅ Completed)
*   [x] Perform feature engineering (time of day, interaction terms).
*   [x] Train XGBoost regressor (`train_model.py`).
*   [x] Evaluate model performance (MAE, RMSE, R²).
*   [x] Serialize model for deployment (`.pkl`).

### Phase 4: User Interface & Deployment (✅ Completed)
*   [x] Develop interactive dashboard using Streamlit.
*   [x] Integrate trained model for real-time inference.
*   [x] Implement dynamic input sliders for simulation.

### Phase 5: Documentation & Polish (🔄 In Progress)
*   [x] Create comprehensive `README.md`.
*   [x] Create `demo_script.md`.
*   [ ] Finalize `references.md`.
*   [ ] Code cleanup and commenting.

## 🚀 Future Enhancements
*   **Hardware Integration**: Connect real IoT sensors (ESP32 + BME680 + UV Sensor) to feed live data instead of APIs.
*   **Mobile App**: Port the dashboard to a mobile-friendly React Native app.
*   **Alert System**: Send SMS/Email alerts when safe exposure time drops below a threshold.
*   **User Profiles**: Personalized recommendations based on skin type and health conditions.
