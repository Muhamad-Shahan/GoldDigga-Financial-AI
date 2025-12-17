# 💰 GoldDigga: Financial Time-Series Forecaster

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-link-here.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Model](https://img.shields.io/badge/Model-Random_Forest_Regressor-green.svg)](https://scikit-learn.org/)

## 📊 Executive Summary
Predicting financial markets is notoriously difficult due to volatility and noise. Traditional regression often fails because it ignores the temporal sequence of data.

**GoldDigga AI** is a **Time-Series Forecasting System** that predicts the daily price of Gold (GLD). Unlike simple regression, this system utilizes **Lag Features (t-1)** to model the sequential dependency of asset prices. By analyzing correlations with **Silver (SLV)**, **Crude Oil (USO)**, the **S&P 500 (SPX)**, and **EUR/USD** exchange rates, the model achieves an **R² Score of ~92%** on unseen future data.

> **[🔴 Live Dashboard Demo](https://your-app-link-here.streamlit.app/)**

## 🛠️ Technical Architecture
This project solves the "Look-Ahead Bias" common in beginner financial models by implementing a strict Time-Series Split.

### 1. Methodology
* **Time-Series Split:** Data is split chronologically (First 80% for training, Last 20% for testing). No random shuffling ensures the model predicts the *future* based only on the *past*.
* **Lag Features:** The model inputs are shifted by 1 day.
    * *Input:* Market Data from **Yesterday**.
    * *Target:* Gold Price **Today**.
    * This mimics real-world trading scenarios where tomorrow's price is unknown.

### 2. The Model
* **Algorithm:** Random Forest Regressor (Ensemble Learning).
* **Hyperparameters:** `n_estimators=100`.
* **Performance:**
    * **R² Score:** 0.92 (Explains 92% of price variance).
    * **Baseline:** significantly outperforms a naive "Random Walk" prediction.

## 📉 Market Correlation Analysis
The model discovered strong positive correlations, particularly between **Gold and Silver**, validating the "Precious Metals" market basket theory.

| Asset Pair | Correlation Coefficient | Relationship |
|:----------:|:-----------------------:|:------------:|
| **GLD / SLV** | **0.87** | 🟢 Strong Positive |
| GLD / SPX | 0.04 | ⚪ Neutral / Decoupled |
| GLD / USO | -0.19 | 🔴 Weak Negative |

## 💻 Installation & Usage

**Prerequisites:** Python 3.8+

```bash
# 1. Clone the repo
git clone [https://github.com/Muhammad-Shahan/Gold-Price-Time-Series-Forecaster.git](https://github.com/Muhammad-Shahan/Gold-Price-Time-Series-Forecaster.git)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Dashboard
streamlit run app.py
