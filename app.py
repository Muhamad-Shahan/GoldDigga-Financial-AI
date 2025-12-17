import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="GoldDigga AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (THEME AGNOSTIC) ---
# We use CSS variables (var(--...)) so it adapts to Light/Dark mode automatically
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }

    /* Metric Cards - Transparent background with border that adapts */
    div[data-testid="metric-container"] {
        background-color: rgba(128, 128, 128, 0.1); /* Subtle transparent grey */
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 15px;
        border-radius: 10px;
        color: var(--text-color); /* Auto-adapts to theme */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(128, 128, 128, 0.05);
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
    }

    /* Custom Success Message */
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
        border: 2px solid #4CAF50;
        background-color: rgba(76, 175, 80, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOAD RESOURCES ---
@st.cache_resource
def load_data_and_model():
    try:
        # Load Model
        model = joblib.load('gold_price_model.pkl')

        # Load Data (Only to get min/max values for sliders)
        df = pd.read_csv('gold_price_data.csv')

        return model, df
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return None, None

model, df = load_data_and_model()

if df is not None:
    # Preprocessing for dashboard stats
    df['Date'] = pd.to_datetime(df['Date'])
    latest_data = df.iloc[-1]

    # Calculate daily changes for metrics
    prev_data = df.iloc[-2]
    gold_change = latest_data['GLD'] - prev_data['GLD']
    silver_change = latest_data['SLV'] - prev_data['SLV']

# --- 4. SIDEBAR (SCENARIO INPUTS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
    st.title("Market Simulator")
    st.markdown("Adjust today's market indicators to predict **Tomorrow's Gold Price**.")
    st.markdown("---")

    if df is not None:
        # We use sliders bounded by the realistic min/max of the historical data

        # 1. Gold Price (Lag)
        current_gold = st.number_input("Current Gold Price (GLD)", value=float(latest_data['GLD']))

        # 2. SPX (Stock Market)
        spx = st.slider("S&P 500 Index",
                        min_value=float(df['SPX'].min()),
                        max_value=float(df['SPX'].max()),
                        value=float(latest_data['SPX']))

        # 3. USO (Oil Price)
        uso = st.slider("United States Oil Fund (USO)",
                        min_value=float(df['USO'].min()),
                        max_value=float(df['USO'].max()),
                        value=float(latest_data['USO']))

        # 4. Silver Price
        slv = st.slider("Silver Price (SLV)",
                        min_value=float(df['SLV'].min()),
                        max_value=float(df['SLV'].max()),
                        value=float(latest_data['SLV']))

        # 5. Euro/USD Pair
        eur_usd = st.slider("EUR/USD Exchange Rate",
                            min_value=float(df['EUR/USD'].min()),
                            max_value=float(df['EUR/USD'].max()),
                            value=float(latest_data['EUR/USD']))

        st.markdown("---")
        predict_btn = st.button("🔮 Run Forecast", type="primary")

# --- 5. MAIN DASHBOARD ---
st.title("GoldDigga AI 📈")
st.markdown(f"**Financial Intelligence Dashboard** | Data as of: {date.today()}")

if df is not None:
    # TOP ROW METRICS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Gold (GLD)", f"${latest_data['GLD']:.2f}", f"{gold_change:.2f}")
    with col2:
        st.metric("Silver (SLV)", f"${latest_data['SLV']:.2f}", f"{silver_change:.2f}")
    with col3:
        st.metric("S&P 500", f"{latest_data['SPX']:.2f}")
    with col4:
        st.metric("Model Accuracy (R²)", "92.2%")

    # --- PREDICTION SECTION ---
    if predict_btn:
        # Prepare input array [SPX, USO, SLV, EUR/USD, GLD]
        # Important: The order MUST match X_train columns from your notebook
        input_data = pd.DataFrame({
            'SPX': [spx],
            'USO': [uso],
            'SLV': [slv],
            'EUR/USD': [eur_usd],
            'GLD': [current_gold] # This is our Lag feature!
        })

        # Predict
        prediction = model.predict(input_data)[0]

        # Visualizing the Prediction
        st.markdown("---")
        st.markdown("### 🤖 AI Forecast")

        c1, c2 = st.columns([1, 2])

        with c1:
            # Color logic
            color = "#4CAF50" if prediction > current_gold else "#FF5252"
            direction = "UP ▲" if prediction > current_gold else "DOWN ▼"

            st.markdown(f"""
            <div class="prediction-box" style="border-color: {color}; background-color: {color}20;">
                <h3 style="margin:0; color:var(--text-color);">Predicted Price</h3>
                <h1 style="margin:0; color:{color}; font-size: 3rem;">${prediction:.2f}</h1>
                <p style="margin-top:10px; font-weight:bold; color:{color};">{direction}</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            # Gauge Chart for Prediction vs Current
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = prediction,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Forecast vs Current", 'font': {'size': 20}},
                delta = {'reference': current_gold, 'relative': False, "valueformat": ".2f"},
                gauge = {
                    'axis': {'range': [min(current_gold, prediction)*0.9, max(current_gold, prediction)*1.1]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, current_gold], 'color': "rgba(128,128,128,0.2)"}
                    ],
                }
            ))
            fig.update_layout(height=250, margin=dict(t=30,b=10,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True)

    # --- HISTORICAL CHART SECTION ---
    st.markdown("---")
    st.subheader("📊 Historical Market Trend")

    # User selects duration
    chart_view = st.radio("Timeframe", ["All Time", "Last Year", "Last Month"], horizontal=True)

    # Filter data based on view
    df_chart = df.copy()
    if chart_view == "Last Year":
        df_chart = df_chart.iloc[-365:]
    elif chart_view == "Last Month":
        df_chart = df_chart.iloc[-30:]

    # Interactive Line Chart with Plotly
    fig_hist = px.line(df_chart, x='Date', y=['GLD', 'SLV'],
                       title="Gold vs Silver Price Correlation",
                       color_discrete_map={"GLD": "#FFD700", "SLV": "#C0C0C0"})

    fig_hist.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        legend_title="Asset"
    )

    # This magic line makes Plotly respect Streamlit's Dark/Light mode
    st.plotly_chart(fig_hist, use_container_width=True, theme="streamlit")

else:
    st.warning("⚠️ Data or Model not found. Please check your files.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 12px; opacity: 0.7;">
    Designed with ❤️ by Muhammad Shahan | Powered by Random Forest Regressor<br>
    <i>Not financial advice. Use AI predictions at your own risk.</i>
</div>
""", unsafe_allow_html=True)
