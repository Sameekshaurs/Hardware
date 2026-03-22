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

# ================= ⚡ BACKGROUND + UI =================
st.markdown("""
<style>

/* 🎬 CINEMATIC BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 30% 20%, #0a1a2f, #000000 70%);
    overflow: hidden;
}

/* ⚡ ELECTRIC ENERGY LAYER */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: linear-gradient(
        120deg,
        rgba(0,255,255,0.05),
        transparent,
        rgba(0,255,255,0.08)
    );
    animation: energyFlow 6s infinite linear;
    z-index: 0;
}

/* ⚡ GLOW PULSE */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(circle, rgba(0,255,255,0.08), transparent 70%);
    animation: pulse 4s infinite ease-in-out;
    z-index: 0;
}

/* ENERGY FLOW ANIMATION */
@keyframes energyFlow {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* PULSE ANIMATION */
@keyframes pulse {
    0% { opacity: 0.2; }
    50% { opacity: 0.5; }
    100% { opacity: 0.2; }
}

/* KEEP CONTENT ABOVE */
.main, header, section {
    position: relative;
    z-index: 1;
}

/* 💎 GLASS CARDS WITH NEON EDGE */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    box-shadow:
        0 0 10px rgba(0,255,255,0.4),
        0 0 30px rgba(0,255,255,0.2);
    text-align: center;
}

/* 🎬 CINEMATIC TITLE */
.title {
    font-size: 46px;
    text-align: center;
    font-weight: bold;
    color: #00f2ff;
    text-shadow:
        0 0 10px #00f2ff,
        0 0 40px #00f2ff,
        0 0 80px rgba(0,255,255,0.6);
    margin-bottom: 20px;
}

/* 🚨 ALERT (INTENSE) */
.blink {
    animation: blink-animation 0.6s steps(2, start) infinite;
    color: #ff2e2e;
    font-size: 36px;
    text-align: center;
    font-weight: bold;
    text-shadow: 0 0 20px red;
}

@keyframes blink-animation {
    to { visibility: hidden; }
}

/* ⚡ SCREEN FLASH ON FAULT */
.flash {
    animation: flash-bg 0.25s ease 3;
}

@keyframes flash-bg {
    0% { background-color: white; }
    100% { background-color: transparent; }
}

/* 🎛 SIDEBAR (DARK CONTROL PANEL) */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #050a14, #000000);
    box-shadow: 0 0 30px cyan;
}

/* 🌫 SUBTLE FOG EFFECT */
.main::before {
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at bottom, rgba(0,0,0,0.6), transparent);
    z-index: 0;
}

</style>
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

    # ⚡ lightning flash
    st.markdown("""
    <script>
    document.body.classList.add('flash');
    setTimeout(() => {
        document.body.classList.remove('flash');
    }, 300);
    </script>
    """, unsafe_allow_html=True)

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card"><h3>Voltage</h3><h1>{round(voltage,2)} V</h1></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card"><h3>Current</h3><h1>{round(current,2)} A</h1></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card"><h3>Status</h3><h1>{fault}</h1></div>', unsafe_allow_html=True)

st.markdown(f"### 📍 Fault Location: **{location}**")

# ================= 🌍 MAP =================
st.subheader("🌍 Grid Visualization")

lat = [node_locations[n][0] for n in selected_nodes]
lon = [node_locations[n][1] for n in selected_nodes]

colors = []
for n in selected_nodes:
    if n == location:
        colors.append("red")   # fault node
    else:
        colors.append("cyan")

fig_map = go.Figure(go.Scattermapbox(
    lat=lat,
    lon=lon,
    mode='markers+text',
    marker=dict(size=14, color=colors),
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