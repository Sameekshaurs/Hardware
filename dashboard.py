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
MODE = "API"
API_URL = "https://fault-backend-itqk.onrender.com/data"

# ================= ⚡ BACKGROUND + UI =================
st.markdown("""
<style>

/* 🌌 DEEP CINEMATIC BASE */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #020617, #000000 80%);
}

/* ⚡ ELECTRIC ENERGY FLOW */
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
    animation: energyFlow 5s infinite linear;
    z-index: 0;
}

/* ⚡ PULSE GLOW */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(circle, rgba(0,255,255,0.08), transparent 70%);
    animation: pulse 3s infinite ease-in-out;
    z-index: 0;
}

/* ENERGY FLOW */
@keyframes energyFlow {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* PULSE */
@keyframes pulse {
    0% { opacity: 0.2; }
    50% { opacity: 0.6; }
    100% { opacity: 0.2; }
}

/* ⚡ LIGHTNING BOLT */
.lightning {
    position: fixed;
    top: 0;
    left: 50%;
    width: 2px;
    height: 100%;
    background: white;
    opacity: 0;
    animation: lightningFlash 0.2s ease 2;
    z-index: 999;
}

@keyframes lightningFlash {
    0% { opacity: 0; }
    50% { opacity: 1; box-shadow: 0 0 20px white; }
    100% { opacity: 0; }
}

/* 🔴 FAULT NODE PULSE */
.pulse-node {
    animation: nodePulse 1s infinite;
}

@keyframes nodePulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.6; }
    100% { transform: scale(1); opacity: 1; }
}

/* 💎 CARDS */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    box-shadow:
        0 0 10px rgba(0,255,255,0.5),
        0 0 40px rgba(0,255,255,0.2);
    text-align: center;
}

/* 🎬 TITLE */
.title {
    font-size: 48px;
    text-align: center;
    font-weight: bold;
    color: #00f2ff;
    text-shadow:
        0 0 10px #00f2ff,
        0 0 50px #00f2ff,
        0 0 100px rgba(0,255,255,0.6);
}

/* 🚨 ALERT */
.blink {
    animation: blink-animation 0.5s steps(2, start) infinite;
    color: #ff2e2e;
    font-size: 38px;
    text-align: center;
    font-weight: bold;
    text-shadow: 0 0 30px red;
}

@keyframes blink-animation {
    to { visibility: hidden; }
}

/* 🎛 SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #020617, #000000);
    box-shadow: 0 0 30px cyan;
}

/* KEEP CONTENT ABOVE */
.main, header, section {
    position: relative;
    z-index: 1;
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
    st.session_state.data = pd.DataFrame(columns=["Time", "NodeA_V", "NodeA_C", "NodeB_V", "NodeB_C"])

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
            return (
                res.get("nodeA_voltage", 0),
                res.get("nodeA_current", 0),
                res.get("nodeB_voltage", 0),
                res.get("nodeB_current", 0)
            )
        except:
            return 0, 0, 0, 0
    else:
        return (
            random.uniform(210, 240),
            random.uniform(0, 10),
            random.uniform(210, 240),
            random.uniform(0, 10)
        )

def predict_fault(voltage, current):
    if voltage < 200:
        return "UNDER VOLTAGE FAULT"
    elif current > threshold:
        return "OVER CURRENT FAULT"
    else:
        return "NORMAL"

nodeA_v, nodeA_c, nodeB_v, nodeB_c = get_data()

# ================= STORE DATA =================
new_data = {
    "Time": len(st.session_state.data),
    "NodeA_V": nodeA_v,
    "NodeA_C": nodeA_c,
    "NodeB_V": nodeB_v,
    "NodeB_C": nodeB_c
}

st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_data])],
    ignore_index=True
)

df = st.session_state.data.tail(50)

# ================= FAULT =================
def detect_line_fault(vA, cA, vB, cB):
    # Case 1: Everything normal
    if vA >= 200 and vB >= 200 and cA < threshold and cB < threshold:
        return "NORMAL ✅", "-"

    # Case 2: Voltage drop from A → B
    if vA >= 200 and vB < 200:
        return "FAULT BETWEEN NODE A → NODE B ⚠️", "Between A-B"

    # Case 3: Both low → upstream issue
    if vA < 200 and vB < 200:
        return "UPSTREAM FAULT ⚠️", "Before Node A"

    # Case 4: High current spike
    if cA > threshold or cB > threshold:
        return "OVER CURRENT FAULT ⚡", "Between A-B"

    return "NORMAL ✅", "-"


# Apply logic
overall_fault, location = detect_line_fault(nodeA_v, nodeA_c, nodeB_v, nodeB_c)

# Store location
st.session_state.fault_location = location

# ================= ALERT =================
if overall_fault != "NORMAL ✅":
    # 🚨 blinking alert
    st.markdown('<div class="blink">🚨 FAULT DETECTED 🚨</div>', unsafe_allow_html=True)

    # ⚡ lightning strike overlay
    st.markdown('<div class="lightning"></div>', unsafe_allow_html=True)

    # ⚡ screen flash effect
    st.markdown("""
    <script>
    document.body.classList.add('flash');
    setTimeout(() => {
        document.body.classList.remove('flash');
    }, 300);
    </script>
    """, unsafe_allow_html=True)
# ================= METRICS =================
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="card"><h3>Node A Voltage</h3><h1>{round(nodeA_v,2)} V</h1></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card"><h3>Node A Current</h3><h1>{round(nodeA_c,2)} A</h1></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card"><h3>Node B Voltage</h3><h1>{round(nodeB_v,2)} V</h1></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card"><h3>Node B Current</h3><h1>{round(nodeB_c,2)} A</h1></div>', unsafe_allow_html=True)

# 🔥 CENTER STATUS CARD
st.markdown(f'''
<div class="card" style="margin-top:20px;">
    <h3>System Status</h3>
    <h1>{overall_fault}</h1>
</div>
''', unsafe_allow_html=True)

# Location
st.markdown(f"### 📍 Fault Location: **{location}**")
# ================= 🌍 MAP =================
st.subheader("🌍 Grid Visualization")

lat = [node_locations[n][0] for n in selected_nodes]
lon = [node_locations[n][1] for n in selected_nodes]

fig_map = go.Figure()

# 🔗 BASE GRID LINES (dim background lines)
line_lat = []
line_lon = []

for i in range(len(lat) - 1):
    line_lat += [lat[i], lat[i+1], None]
    line_lon += [lon[i], lon[i+1], None]

fig_map.add_trace(go.Scattermapbox(
    lat=line_lat,
    lon=line_lon,
    mode='lines',
    line=dict(width=2, color='rgba(0,255,255,0.3)'),
    hoverinfo='none'
))

# 🔥 HIGHLIGHT FAULT LINE (Between A-B)
if location == "Between A-B" and len(lat) >= 2:
    fig_map.add_trace(go.Scattermapbox(
        lat=[lat[0], lat[1]],
        lon=[lon[0], lon[1]],
        mode='lines',
        line=dict(width=6, color='red'),
        hoverinfo='none'
    ))

# ⚡ CURRENT FLOW (moving dots illusion)
flow_lat = []
flow_lon = []

for i in range(len(lat) - 1):
    mid_lat = (lat[i] + lat[i+1]) / 2
    mid_lon = (lon[i] + lon[i+1]) / 2
    flow_lat.append(mid_lat)
    flow_lon.append(mid_lon)

fig_map.add_trace(go.Scattermapbox(
    lat=flow_lat,
    lon=flow_lon,
    mode='markers',
    marker=dict(size=8, color='cyan'),
    hoverinfo='none'
))

# 🔴 NODES (highlight based on fault)
colors = []
sizes = []

for i, n in enumerate(selected_nodes):
    if location == "Before Node A" and i == 0:
        colors.append("red")
        sizes.append(24)
    elif location == "Between A-B":
        colors.append("yellow")  # indicate segment fault
        sizes.append(16)
    else:
        colors.append("cyan")
        sizes.append(12)

fig_map.add_trace(go.Scattermapbox(
    lat=lat,
    lon=lon,
    mode='markers+text',
    marker=dict(size=sizes, color=colors),
    text=selected_nodes,
    textposition="top center"
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
    fig1 = px.line(df, x="Time", y=["NodeA_V", "NodeB_V"], title="Voltage Trend (Node A vs Node B)")
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(df, x="Time", y=["NodeA_C", "NodeB_C"], title="Current Trend (Node A vs Node B)")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# ================= HISTORY =================
# ================= HISTORY =================

# Node A fault
if faultA != "NORMAL":
    new_fault_A = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Fault Type": faultA,
        "Location": "Node A",
        "Voltage": round(nodeA_v, 2),
        "Current": round(nodeA_c, 2)
    }])

    st.session_state.fault_history = pd.concat(
        [st.session_state.fault_history, new_fault_A],
        ignore_index=True
    )

# Node B fault
if faultB != "NORMAL":
    new_fault_B = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Fault Type": faultB,
        "Location": "Node B",
        "Voltage": round(nodeB_v, 2),
        "Current": round(nodeB_c, 2)
    }])

    st.session_state.fault_history = pd.concat(
        [st.session_state.fault_history, new_fault_B],
        ignore_index=True
    )

# keep last 20 records
st.session_state.fault_history = st.session_state.fault_history.tail(20)

# display
st.subheader("📜 Fault History")
st.dataframe(st.session_state.fault_history, use_container_width=True)