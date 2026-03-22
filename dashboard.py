import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# ================= CONFIG =================
MODE = "DEMO"   # 🔁 change to "REAL" when using ESP32 locally

# ================= PAGE =================
st.set_page_config(layout="wide")
st.title("⚡ AI-Based Fault Detection Dashboard")

# ================= DATA STORAGE =================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Voltage", "Current"])

# ================= DATA SOURCE =================
def get_data():
    if MODE == "REAL":
        try:
            import serial
            ser = serial.Serial("COM23", 9600, timeout=1)
            line = ser.readline().decode().strip()
            parts = line.split(",")

            voltage = float(parts[0])
            current = float(parts[1])

            return voltage, current
        except:
            return 0, 0

    else:
        # DEMO DATA
        voltage = random.uniform(210, 240)
        current = random.uniform(0, 10)
        return voltage, current

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
fault = "NO FAULT ✅"
location = "-"

if voltage < 200 or current > 8:
    fault = "FAULT DETECTED ⚠️"
    location = f"Node {random.randint(1,5)}"

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

col1.metric("Voltage (V)", round(voltage, 2))
col2.metric("Current (A)", round(current, 2))
col3.metric("Status", fault)

st.subheader(f"📍 Fault Location: {location}")

# ================= GRAPHS =================
fig1 = px.line(df, x="Time", y="Voltage", title="Voltage vs Time")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(df, x="Time", y="Current", title="Current vs Time")
st.plotly_chart(fig2, use_container_width=True)

# ================= AUTO REFRESH =================
time.sleep(2)
st.rerun()
