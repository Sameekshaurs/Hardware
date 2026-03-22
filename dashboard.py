import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ================= AUTO REFRESH =================
st_autorefresh(interval=2000, key="refresh")

# ================= CONFIG =================
MODE = "DEMO"
API_URL = "https://fault-backend-itqk.onrender.com/data"

# ================= ⚡ ELECTRIC BACKGROUND =================
st.markdown("""
<style>

/* animated electric grid background */
body {
    background: radial-gradient(circle at center, #0a0f1f, #000000);
    color: white;
}

/* moving electric lines */
.electric-bg {
    position: fixed;
    width: 100%;
    height: 100%;
    background-image: repeating-linear-gradient(
        45deg,
        rgba(0,255,255,0.05) 0px,
        rgba(0,255,255,0.05) 2px,
        transparent 2px,
        transparent 40px
    );
    animation: moveLines 5s linear infinite;
    z-index: -1;
}

@keyframes moveLines {
    from { background-position: 0 0; }
    to { background-position: 120px 120px; }
}

/* glass cards */
.card {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 25px rgba(0,255,255,0.3);
    text-align: center;
}

/* glowing title */
.title {
    font-size: 42px;
    text-align: center;
    font-weight: bold;
    color: #00f2ff;
    text-shadow: 0 0 30px #00f2ff;
}

/* blinking alert */
.blink {
    animation: blink-animation 1s steps(2, start) infinite;
    color: red;
    font-size: 32px;
    text-align: center;
    font-weight: bold;
}

@keyframes blink-animation {
    to { visibility: hidden; }
}

/* sidebar glow */
section[data-testid="stSidebar"] {
    background-color: #0a0f1f;
    box-shadow: 0 0 20px cyan;
}

</style>

<div class="electric-bg"></div>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<div class="title">⚡ Smart Fault Detection System</div>', unsafe_allow_html=True)

# ================= 🎛 CONTROL PANEL =================
st.sidebar.title("🎛 Control Panel")

selected_nodes = st.sidebar.multiselect(
    "Active Nodes",
    ["Line Node 1","Line Node 2","Line Node 3","Line Node 4","Line Node 5"],
    default=["Line Node 1","Line Node 2"]
)

threshold = st.sidebar.slider("Current Threshold", 1, 15, 8)

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
    elif current > threshold:
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
        st.session_state.fault_location = random.choice(selected_nodes)

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

# ================= 🌍 CUSTOM MAP =================
st.subheader("🌍 Grid Visualization")

lat = [node_locations[n][0] for n in selected_nodes]
lon = [node_locations[n][1] for n in selected_nodes]

fig_map = go.Figure(go.Scattermapbox(
    lat=lat,
    lon=lon,
    mode='markers+text',
    marker=dict(size=12, color="cyan"),
    text=selected_nodes
))

fig_map.update_layout(
    mapbox_style="carto-darkmatter",
    mapbox_zoom=4,
    mapbox_center={"lat": 13, "lon": 78},
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig_map, use_container_width=True)

# ================= GRAPHS =================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df, x="Time", y="Voltage")
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(df, x="Time", y="Current")
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