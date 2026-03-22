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
MODE = "DEMO"
API_URL = "https://fault-backend-itqk.onrender.com/data"

# ================= BACKGROUND + UI =================
st.markdown("""
<style>

/* Animated gradient background */
body {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #00c6ff);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass cards */
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
    text-align: center;
}

/* Title */
.title {
    font-size: 42px;
    text-align: center;
    font-weight: bold;
    color: #00f2ff;
    text-shadow: 0 0 25px #00f2ff;
}

/* Blinking alert */
.blink {
    animation: blink-animation 1s steps(2, start) infinite;
    color: red;
    font-size: 30px;
    text-align: center;
    font-weight: bold;
}

@keyframes blink-animation {
    to { visibility: hidden; }
}

/* Table styling */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<div class="title">⚡ Smart Fault Detection System</div>', unsafe_allow_html=True)

# ================= NODE LOCATIONS =================
node_locations = {
    "Line Node 1": (12.9716, 77.5946),
    "Line Node 2": (12.2958, 76.6394),
    "Line Node 3": (13.0827, 80.2707),
    "Line Node 4": (17.3850, 78.4867),
    "Line Node 5": (19.0760, 72.8777)
}

# ================= SESSION =================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Voltage", "Current"])

if "fault_location" not in st.session_state:
    st.session_state.fault_location = "-"

if "fault_history" not in st.session_state:
    st.session_state.fault_history = pd.DataFrame(
        columns=["Timestamp", "Fault Type", "Location", "Voltage", "Current"]
    )

# ================= DATA =================
def get_data():
    if MODE == "API":
        try:
            res = requests.get(API_URL).json()
            return res["voltage"], res["current"]
        except:
            return 0, 0
    else:
        return random.uniform(210, 240), random.uniform(0, 10)

def predict_fault(voltage, current):
    if voltage < 200:
        return "UNDER VOLTAGE FAULT"
    elif current > 8:
        return "OVER CURRENT FAULT"
    else:
        return "NORMAL"

voltage, current = get_data()

# ================= STORE DATA =================
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

# ================= FAULT =================
prediction = predict_fault(voltage, current)

if prediction == "NORMAL":
    fault = "NORMAL ✅"
    st.session_state.fault_location = "-"
else:
    fault = f"{prediction} ⚠️"
    if st.session_state.fault_location == "-":
        st.session_state.fault_location = f"Line Node {random.randint(1,5)}"

location = st.session_state.fault_location

# ================= ALERT =================
if prediction != "NORMAL":
    st.markdown('<div class="blink">🚨 FAULT DETECTED 🚨</div>', unsafe_allow_html=True)

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card"><h3>Voltage</h3><h1>{round(voltage,2)} V</h1></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card"><h3>Current</h3><h1>{round(current,2)} A</h1></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card"><h3>Status</h3><h1>{fault}</h1></div>', unsafe_allow_html=True)

st.markdown(f"### 📍 Fault Location: **{location}**")

# ================= MAP =================
if location != "-":
    lat, lon = node_locations.get(location, (12.9716, 77.5946))
    st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))

# ================= GRAPHS =================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df, x="Time", y="Voltage", title="Voltage vs Time")
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(df, x="Time", y="Current", title="Current vs Time")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# ================= HISTORY =================
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
    ).tail(20)

st.subheader("📜 Fault History")
st.dataframe(st.session_state.fault_history, use_container_width=True)