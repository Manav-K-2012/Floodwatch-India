import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="FloodWatch India", page_icon="🌊", layout="wide")

st.title("FloodWatch India")
st.write("Real-time flood monitoring dashboard for India")

# Sidebar
st.sidebar.header("Input Parameters")
rainfall = st.sidebar.slider("Rainfall (mm)", 0, 500, 120)
river_level = st.sidebar.slider("River Level (m)", 0.0, 20.0, 5.5)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 80)
temperature = st.sidebar.slider("Temperature (C)", 10, 50, 30)

# Check files
st.sidebar.write("---")
if os.path.exists('flood_model.pkl'):
    st.sidebar.success("Model Found: flood_model.pkl")
else:
    st.sidebar.warning("Using demo logic (no model)")

# Prediction button
if st.button("Check Flood Risk", type="primary"):
    try:
        # Try to use real model if exists
        if os.path.exists('flood_model.pkl'):
            model = pickle.load(open('flood_model.pkl', 'rb'))
            # Assuming model needs 4 features - change as per your model
            data = [[rainfall, river_level, humidity, temperature]]
            prediction = model.predict(data)
            result = prediction[0]
        else:
            # Demo logic if model not found
            if rainfall > 200 or river_level > 12:
                result = 2
            elif rainfall > 100 or river_level > 7:
                result = 1
            else:
                result = 0

        # Show result
        if result == 2 or result == "High" or result == 2.0:
            st.error("🔴 HIGH FLOOD RISK - Evacuate Low Areas!")
        elif result == 1 or result == "Medium" or result == 1.0:
            st.warning("🟡 MEDIUM RISK - Stay Alert")
        else:
            st.success("🟢 LOW RISK - Safe")

    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.info("Using simple logic")
        if rainfall > 200 or river_level > 12:
            st.error("HIGH FLOOD RISK")
        else:
            st.success("LOW RISK")

# Map
st.write("---")
st.subheader("Flood Prone Areas - Thane, Maharashtra")
map_data = pd.DataFrame({
    'lat': [19.2183, 19.0760, 19.2094],
    'lon': [72.9781, 72.8777, 73.0934]
})
st.map(map_data)

st.caption("Built by Manav | FloodWatch India v1.0")
