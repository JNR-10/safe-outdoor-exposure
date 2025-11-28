# ☀️ Adaptive UV & Air Quality Co-Optimization System

## 📖 Overview
This project is an **IoT-based Adaptive UV and Air Quality Co-Optimization System** designed to help users safely navigate outdoor environments. By integrating real-time environmental data (UV Index, PM2.5, Temperature, Humidity, etc.) with machine learning, the system predicts **safe outdoor exposure times** to minimize health risks associated with harmful UV radiation and poor air quality.

The system features a **live dashboard** for real-time monitoring and decision support, making it a valuable tool for health-conscious individuals and smart city applications.

## ✨ Key Features
- **Real-time Data Fetching**: Automatically aggregates UV Index, Air Quality (PM2.5), and weather data for multiple cities.
- **Predictive Analytics**: Uses an **XGBoost** regression model to calculate safe exposure duration based on current environmental conditions.
- **Interactive Dashboard**: A user-friendly **Streamlit** interface to visualize data, adjust parameters, and view predictions instantly.
- **Historical Data Analysis**: Capabilities to process and analyze historical environmental trends.
- **Scalable Architecture**: Modular design separating data ingestion, processing, model training, and deployment.

## 🛠️ Technologies Used
- **Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: XGBoost, Scikit-learn, Joblib
- **Visualization**: Matplotlib, Seaborn
- **Web Framework**: Streamlit
- **APIs**: Open-Meteo (UV), AirNow (Air Quality), Nominatim (Geocoding)

## 📂 Project Structure
```
IoT Project/
├── 1_Software_Architecture_Flowchart.png
├── ... (Architecture Images)
├── README.md                   # Project Documentation
├── requirements.txt            # Python Dependencies
├── .env                        # Environment Variables (API Keys)
├── src/                        # Source Code
│   ├── data_fetch.py           # Data Ingestion Script
│   ├── feature_engineering.py  # Feature Processing Logic
│   ├── train_model.py          # ML Model Training Script
│   ├── deploy_predict.py       # Prediction Logic
│   └── sensors.py              # Sensor Interface (Mock/Real)
├── dashboard/                  # Web Application
│   └── streamlit_app.py        # Streamlit Dashboard Entry Point
├── data/                       # Data Storage
│   ├── raw/                    # Raw CSVs from APIs
│   └── processed/              # Cleaned Data for Training
├── models/                     # Serialized ML Models
│   └── safe_exposure_model.pkl # Trained XGBoost Model
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "IoT Project"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your configuration:
```ini
# .env
AIRNOW_KEY=your_airnow_api_key_here
CITIES=San Jose, San Francisco, New York
COUNTRY=US
DAYS=30
```
> **Note**: You can get an AirNow API key from [AirNow API](https://docs.airnowapi.org/).

## 🏃 Usage

### 1. Fetch Data
Collect historical or real-time data to build your dataset:
```bash
python src/data_fetch.py
```
This will save data to `data/raw/merged_uv_aq_multi.csv`.

### 2. Train the Model
Train the XGBoost model using the fetched data:
```bash
python src/train_model.py
```
The trained model will be saved to `models/safe_exposure_model.pkl`.

### 3. Run the Dashboard
Launch the interactive web application:
```bash
streamlit run dashboard/streamlit_app.py
```
Access the dashboard in your browser at `http://localhost:8501`.

## 📊 Model Performance
The system uses an XGBoost regressor which has been evaluated for accuracy in predicting safe exposure times.

| Metric | Value |
| :--- | :--- |
| **MAE** | 0.064 |
| **RMSE** | 0.603 |
| **R²** | 0.998 |


