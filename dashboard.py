import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import random
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ================= AUTO REFRESH =================
st_autorefresh(interval=2000, key="refresh")

# ================= CONFIG =================
MODE = "DEMO"   # change to "API" later
API_URL = "http://127.0.0.1:5000/data"

# ================= NODE LOCATIONS =================
node_locations = {
    "Line Node 1": (12.9716, 77.5946),
    "Line Node 2": (12.2958, 76.6394),
    "Line Node 3": (13.0827, 80.2707),
    "Line Node 4": (17.3850, 78.4867),
    "Line Node 5": (19.0760, 72.8777)
}

# ================= PAGE =================
st.set_page_config(layout="wide")
st.title("⚡ Smart Fault Detection System")

# ================= SESSION STATE =================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Voltage", "Current"])

if "fault_location" not in st.session_state:
    st.session_state.fault_location = "-"

if "fault_history" not in st.session_state:
    st.session_state.fault_history = pd.DataFrame(
        columns=["Timestamp", "Fault Type", "Location", "Voltage", "Current"]
    )

# ================= DATA FETCH =================
def get_data():
    if MODE == "API":
        try:
            res = requests.get(API_URL).json()
            return res["voltage"], res["current"]
        except:
            return 0, 0
    else:
        return random.uniform(210, 240), random.uniform(0, 10)

# ================= ML MODEL (SIMULATED) =================
def predict_fault(voltage, current):
    # Replace later with trained ML model
    if voltage < 200:
        return "UNDER VOLTAGE FAULT"
    elif current > 8:
        return "OVER CURRENT FAULT"
    else:
        return "NORMAL"

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

# ================= FAULT DETECTION =================
prediction = predict_fault(voltage, current)

if prediction == "NORMAL":
    fault = "NORMAL ✅"
    st.session_state.fault_location = "-"
else:
    fault = f"{prediction} ⚠️"

    if st.session_state.fault_location == "-":
        st.session_state.fault_location = f"Line Node {random.randint(1,5)}"

location = st.session_state.fault_location

# ================= ALERT (BLINKING) =================
if prediction != "NORMAL":
    st.markdown("""
    <style>
    .blink {
        animation: blink-animation 1s steps(2, start) infinite;
        color: red;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }
    @keyframes blink-animation {
        to { visibility: hidden; }
    }
    </style>
    <div class="blink">🚨 FAULT DETECTED! TAKE ACTION 🚨</div>
    """, unsafe_allow_html=True)

# ================= STORE FAULT HISTORY =================
if prediction != "NORMAL":
    new_fault = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Fault Type": prediction,
        "Location": location,
        "Voltage": round(voltage, 2),
        "Current": round(current, 2)
    }])

    st.session_state.fault_history = pd.concat(
        [st.session_state.fault_history, new_fault],
        ignore_index=True
    ).tail(20)  # keep last 20

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

col1.metric("Voltage (V)", round(voltage, 2))
col2.metric("Current (A)", round(current, 2))
col3.metric("System Status", fault)

st.markdown(f"### 📍 Fault Location: **{location}**")

# ================= MAP =================
if location != "-":
    lat, lon = node_locations.get(location, (12.9716, 77.5946))

    map_df = pd.DataFrame({
        "lat": [lat],
        "lon": [lon]
    })

    st.map(map_df)

# ================= GRAPHS =================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df, x="Time", y="Voltage", title="Voltage vs Time")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(df, x="Time", y="Current", title="Current vs Time")
    st.plotly_chart(fig2, use_container_width=True)

# ================= FAULT HISTORY TABLE =================
st.subheader("📜 Fault History")

st.dataframe(st.session_state.fault_history, use_container_width=True)