import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import os

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Crypto Trends 🚀",
    page_icon="🦆",
    layout="wide"
)

st.title("🚀 Daily Crypto Trends Dashboard")
st.markdown("Monitor high-risk and stable coins directly from **MotherDuck**.")

# -----------------------------------------------------------------------------
# 2. CONNECT TO MOTHERDUCK (Cached)
# -----------------------------------------------------------------------------
# We cache this function so we don't reconnect every time you click a button.
# ttl=600 means "refresh the data every 10 minutes".
@st.cache_data(ttl=600)
def load_data():
    # Retrieve token from environment (safety check)
    token = os.getenv("MOTHERDUCK_TOKEN")
    if not token:
        st.error("🚨 MOTHERDUCK_TOKEN is missing! Run 'export MOTHERDUCK_TOKEN=...' in your terminal.")
        st.stop()

    try:
        # Connect to your specific database
        con = duckdb.connect('md:crypto_database')
        
        # Query the FINAL model (marts), not the raw data
        query = """
            SELECT 
                symbol,
                usd_price,
                daily_change,
                volatility_flag,
                is_high_risk,
                ingested_at
            FROM coin_trends
            ORDER BY abs(daily_change) DESC
        """
        # Return as a Pandas DataFrame
        return con.execute(query).df()
        
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return pd.DataFrame() # Return empty if it fails

# -----------------------------------------------------------------------------
# 3. VISUALIZATION LOGIC
# -----------------------------------------------------------------------------
df = load_data()

if not df.empty:
    # --- KPI SECTION ---
    # We use columns to create a dashboard layout
    kpi1, kpi2, kpi3 = st.columns(3)

    # Top Gainer (Highest Positive Change)
    top_gainer = df.sort_values(by="daily_change", ascending=False).iloc[0]
    kpi1.metric(
        label="🏆 Top Gainer",
        value=f"{top_gainer['symbol'].upper()}",
        delta=f"{top_gainer['daily_change']:.2f}%"
    )

    # Top Loser (Lowest Negative Change)
    top_loser = df.sort_values(by="daily_change", ascending=True).iloc[0]
    kpi2.metric(
        label="💀 Top Loser",
        value=f"{top_loser['symbol'].upper()}",
        delta=f"{top_loser['daily_change']:.2f}%"
    )

    # Risk Count
    risk_count = df[df['is_high_risk'] == True].shape[0]
    kpi3.metric(
        label="⚠️ High Risk Coins",
        value=risk_count,
        delta_color="inverse"
    )

    st.markdown("---")

    # --- CHARTS SECTION ---
    col_chart, col_data = st.columns([2, 1]) # Chart gets 2/3 width, Table gets 1/3

    with col_chart:
        st.subheader("Price vs. Volatility")
        # Scatter plot: X=Price, Y=Change, Color=Risk
        fig = px.scatter(
            df,
            x="usd_price",
            y="daily_change",
            color="volatility_flag",
            size="usd_price", # Bigger bubbles for bigger coins (like BTC)
            hover_data=["symbol"],
            log_x=True,       # Log scale is crucial because BTC ($90k) vs DOGE ($0.10)
            color_discrete_map={
                "🚀 Mooning": "#00CC96",
                "💀 Crashing": "#EF553B",
                "😴 Stable": "#636EFA"
            },
            title="Market Overview (Log Scale)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_data:
        st.subheader("📋 Risky Coins")
        # Show only the high-risk ones in the side table
        risky_df = df[df['is_high_risk'] == True][['symbol', 'daily_change', 'usd_price']]
        st.dataframe(risky_df, use_container_width=True)