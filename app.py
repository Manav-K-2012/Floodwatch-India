import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="FloodWatch India LIVE", page_icon="🌊", layout="wide")
st.title("🌊 FloodWatch India - LIVE + IMD Alerts")

# --- API FUNCTIONS ---
def get_coords(place):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={place}&count=1&language=en&format=json"
        r = requests.get(url, timeout=10).json()
        if r.get('results'):
            f = r['results'][0]
            return f['latitude'], f['longitude'], f"{f['name']}, {f.get('admin1','')}"
        return None, None, None
    except:
        return None, None, None

def get_live_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&past_days=1&hourly=precipitation,wind_speed_10m&daily=precipitation_sum&timezone=Asia/Kolkata"
        r = requests.get(url, timeout=10).json()
        rain_24h = round(sum(r['hourly']['precipitation'][-24:]),1)
        wind = r['hourly']['wind_speed_10m'][-1]
        return rain_24h, wind, r
    except:
        return None, None, None

def get_imd_alert(rain):
    # IMD Official Criteria
    if rain < 7:
        return "🟢 GREEN", "No Warning", "No action needed"
    elif rain < 64.5:
        return "🟢 GREEN", "No Warning", "Light rain expected"
    elif rain < 115.5:
        return "🟡 YELLOW", "Watch", "Be updated - Heavy rain at isolated places"
    elif rain < 204.5:
        return "🟠 ORANGE", "Alert", "Be prepared - Very heavy rain, waterlogging possible"
    else:
        return "🔴 RED", "Warning", "IMD RED ALERT! Extremely heavy rain, FLOOD expected. Take action!"

# --- UI ---
st.sidebar.header("🇮🇳 Search Location")
place = st.sidebar.text_input("District / Village", "Thane")
search = st.sidebar.button("🔍 Check LIVE Flood Status")

if place:
    lat, lon, full_name = get_coords(place)
    if lat is None:
        st.error("Place not found. Try 'Mumbai', 'Thane', 'Agra'")
    else:
        rain, wind, raw = get_live_weather(lat, lon)
        if rain is None:
            st.error("Weather API busy. Try again.")
        else:
            imd_color, imd_title, imd_desc = get_imd_alert(rain)
            
            # Flood score
            river = st.sidebar.slider("River Level (m)", 0.0, 20.0, 4.0)
            soil = st.sidebar.slider("Soil Saturation %", 0, 100, 60)
            score = rain*0.6 + river*4 + soil*0.15

            if score < 25: flood_risk = "🟢 LOW"
            elif score < 50: flood_risk = "🟡 MEDIUM"
            else: flood_risk = "🔴 HIGH"

            # --- DISPLAY ---
            st.success(f"📍 {full_name} | {lat:.2f}, {lon:.2f}")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Live Rain 24h", f"{rain} mm")
            c2.metric("Wind", f"{wind} km/h")
            c3.metric("Flood Risk", flood_risk)

            # IMD ALERT BOX
            if "RED" in imd_color:
                st.error(f"### {imd_color} - IMD {imd_title}\n{imd_desc}")
            elif "ORANGE" in imd_color:
                st.warning(f"### {imd_color} - IMD {imd_title}\n{imd_desc}")
            elif "YELLOW" in imd_color:
                st.info(f"### {imd_color} - IMD {imd_title}\n{imd_desc}")
            else:
                st.success(f"### {imd_color} - IMD {imd_title}\n{imd_desc}")

            # --- AUTO SMS STYLE WARNING ---
            sms_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
            sms_msg = f"""🚨 FLOODWATCH ALERT
Time: {sms_time}
Location: {full_name}
Rainfall: {rain}mm (24h)
IMD: {imd_color} - {imd_title}
Flood Risk: {flood_risk}
River: {river}m

Advice: {imd_desc}

- FloodWatch India
"""
            st.subheader("📲 Auto SMS Warning (Copy & Send to Farmers)")
            st.code(sms_msg, language="text")
            st.download_button("📥 Download SMS as .txt", sms_msg, file_name=f"alert_{place}.txt")

            # For real SMS, integrate Fast2SMS API later
            st.caption("Tip: To send REAL SMS, get free API key from fast2sms.com and we can add 1 line code.")
            
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=10)

st.markdown("---")
st.caption("v3.0 LIVE | Rain: Open-Meteo | IMD Logic: 0-64 Green, 64-115 Yellow, 115-204 Orange, 204+ Red")
