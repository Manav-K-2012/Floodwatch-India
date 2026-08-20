import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="FloodWatch India", page_icon="🌊", layout="wide")

st.title("FloodWatch India")
st.write("Real-time flood monitoring dashboard for India")

st.sidebar.header("Input Parameters")
rainfall = st.sidebar.slider("Rainfall (mm)", 0, 500, 120)
river_level = st.sidebar.slider("River Level (m)", 0.0, 20.0, 5.5)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 80)
temperature = st.sidebar.slider("Temperature (C)", 10, 50, 30)

st.sidebar.write("---")
st.sidebar.info("FloodWatch v1.0 | Thane Region")

if st.button("Check Flood Risk", type="primary"):
    if rainfall > 250 or river_level > 12:
        st.error("🔴 HIGH FLOOD RISK - Evacuate Low Areas!")
        st.write("Immediate action required. Water level critical.")
    elif rainfall > 120 or river_level > 7:
        st.warning("🟡 MEDIUM RISK - Stay Alert")
        st.write("Monitor situation. Possible flooding in 6-12 hours.")
    else:
        st.success("🟢 LOW RISK - Safe")
        st.write("Normal conditions. No flood expected.")

    st.write("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rainfall", f"{rainfall} mm", "High" if rainfall > 150 else "Normal")
    col2.metric("River Level", f"{river_level} m", "Rising" if river_level > 6 else "Stable")
    col3.metric("Humidity", f"{humidity}%")

st.write("---")
st.subheader("Flood Prone Areas - Thane, Maharashtra")
map_data = pd.DataFrame({
    'lat': [19.2183, 19.0760, 19.2094, 19.18],
    'lon': [72.9781, 72.8777, 73.0934, 73.02]
})
st.map(map_data)

st.caption("Built by Manav | FloodWatch India v1.0")
