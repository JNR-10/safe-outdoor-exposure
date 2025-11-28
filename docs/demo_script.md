# 🎬 IoT Project Demo Script

This script outlines the steps to demonstrate the **Adaptive UV & Air Quality Co-Optimization System**.

## 1. Setup & Initialization
*   **Goal**: Show that the environment is ready and dependencies are installed.
*   **Action**:
    *   Open terminal.
    *   Activate virtual environment (if applicable).
    *   Show `.env` file (ensure API keys are set).
    *   Run `pip install -r requirements.txt` to confirm dependencies.

## 2. Data Acquisition (Live Fetch)
*   **Goal**: Demonstrate real-time data aggregation from external APIs.
*   **Action**:
    *   Run: `python src/data_fetch.py`
    *   **Observe**: Terminal output showing data being fetched for configured cities (e.g., San Jose, NYC).
    *   **Verify**: Check `data/raw/merged_uv_aq_multi.csv` timestamp to confirm new data.

## 3. Model Training
*   **Goal**: Show how the machine learning model is trained on the latest data.
*   **Action**:
    *   Run: `python src/train_model.py`
    *   **Observe**:
        *   Data loading and feature engineering logs.
        *   Model training progress (XGBoost).
        *   Evaluation metrics (MAE, RMSE, R²) printed to console.
        *   Confirmation that `models/safe_exposure_model.pkl` is saved.

## 4. Dashboard Walkthrough
*   **Goal**: Demonstrate the user interface and real-time prediction capabilities.
*   **Action**:
    *   Run: `streamlit run dashboard/streamlit_app.py`
    *   Open browser to `http://localhost:8501`.

### Dashboard Features to Highlight:
1.  **Title & Status**: Confirm the app is running ("If you see this text...").
2.  **Input Sliders**:
    *   Adjust **UV Index** (e.g., move from Low to High).
    *   Adjust **PM2.5** (Air Quality).
    *   Adjust **Temperature** and **Humidity**.
3.  **Real-time Prediction**:
    *   Point out the **"Predicted Safe Exposure Time"** metric updating instantly as sliders move.
    *   *Example*: High UV + High PM2.5 -> Low safe exposure time.
4.  **Feature View**: Expand "See computed features" to show the raw input vector being sent to the model.

## 5. Conclusion
*   Summarize the flow: Data -> ML -> Insight.
*   Highlight the system's ability to help users make informed health decisions based on complex environmental data.
