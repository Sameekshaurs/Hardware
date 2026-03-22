import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
import random

# ================= CONFIG =================
MODE = "DEMO"   # change to "API" later

API_URL = "http://127.0.0.1:5000/data"  # your backend later

# ================= PAGE =================
st.set_page_config(layout="wide")
st.title("⚡ Smart Fault Detection System")

# ================= DATA STORAGE =================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Voltage", "Current"])

# ================= DATA FETCH =================
def get_data():
    if MODE == "API":
        try:
            res = requests.get(API_URL).json()
            return res["voltage"], res["current"]
        except:
            return 0, 0
    else:
        # DEMO MODE
        return random.uniform(210, 240), random.uniform(0, 10)

# ================= GET DATA =================
voltage, current = get_data()

new_data = {
    "Time": len(st.session_state.data),
    "Voltage": voltage,
    "Current": current
}

st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_data])],
    ignore_index=True
)

df = st.session_state.data.tail(50)

# ================= FAULT LOGIC =================
fault = "NORMAL ✅"
location = "-"

if voltage < 200 or current > 8:
    fault = "FAULT DETECTED ⚠️"
    location = f"Line Node {random.randint(1,5)}"

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

col1.metric("Voltage (V)", round(voltage, 2))
col2.metric("Current (A)", round(current, 2))
col3.metric("System Status", fault)

st.markdown(f"### 📍 Fault Location: **{location}**")

# ================= GRAPHS =================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df, x="Time", y="Voltage", title="Voltage vs Time")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(df, x="Time", y="Current", title="Current vs Time")
    st.plotly_chart(fig2, use_container_width=True)

# ================= AUTO REFRESH =================
time.sleep(2)
st.rerun()
