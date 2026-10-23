import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="FloodWatch India", page_icon="🌊", layout="centered")

st.title("🌊 FloodWatch India - LIVE Auto Alert System")
st.markdown("### Automatic Flood Detection for Farmers")

# Search box only - NO manual rain/saturation
location = st.text_input("📍 Enter Any Location in India", placeholder="Eg: Thane, Mumbai, Delhi, Kochi")

if st.button("🔍 Check LIVE Flood Status") and location:

    with st.spinner(f"Fetching LIVE data for {location}..."):
        # 1. Get lat/lon of location
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_data = requests.get(geo_url).json()
        
        if "results" not in geo_data:
            st.error("Location not found! Try city name like Thane, Mumbai")
            st.stop()
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        real_name = geo_data["results"][0]["name"]
        state = geo_data["results"][0].get("admin1", "")
        
        # 2. Get LIVE rainfall
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation&daily=precipitation_sum&timezone=auto"
        weather = requests.get(weather_url).json()
        
        live_rain = weather.get("current", {}).get("precipitation", 0.0)
        daily_rain = weather.get("daily", {}).get("precipitation_sum", [0])[0]
        
        # Auto calculate saturation based on rain
        # Logic: >50mm rain = high saturation
        if daily_rain > 50:
            saturation = 90
        elif daily_rain > 20:
            saturation = 70
        elif daily_rain > 5:
            saturation = 50
        else:
            saturation = 30
            
        # 3. IMD Color logic AUTO
        if daily_rain > 50 or live_rain > 15:
            imd_status = "🔴 RED ALERT"
            risk = "HIGH FLOOD RISK"
            color = "red"
        elif daily_rain > 20 or live_rain > 5:
            imd_status = "🟡 YELLOW WATCH"
            risk = "MEDIUM RISK"
            color = "orange"
        else:
            imd_status = "🟢 GREEN - SAFE"
            risk = "LOW RISK - SAFE"
            color = "green"
        
        # SHOW RESULTS
        st.success(f"📍 Location Found: {real_name}, {state}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Live Rain Now", f"{live_rain} mm")
        col2.metric("24hr Rain", f"{daily_rain} mm")
        col3.metric("IMD Status", imd_status)
        
        st.markdown(f"### {risk}")
        
        if "HIGH" in risk:
            st.error(f"🚨 DANGER: Heavy rain detected in {real_name}! Farmers please move to safe place!")
        elif "MEDIUM" in risk:
            st.warning(f"⚠️ Warning: Rain increasing in {real_name}. Stay alert!")
        else:
            st.info(f"✅ Safe: No flood risk in {real_name} today.")
        
        # AUTO SMS MESSAGE
        sms_text = f"""FLOODWATCH INDIA - LIVE ALERT
Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}
Location: {real_name}, {state}
Live Rain: {live_rain} mm
24hr Rain: {daily_rain} mm
Soil Saturation: {saturation}%
IMD Status: {imd_status}
Risk: {risk}
Alert: Stay Safe! - FloodWatch India"""
        
        st.text_area("📲 Auto Generated SMS Alert (Ready to Send to Farmers):", sms_text, height=220)
        
        st.download_button("📥 Download SMS as .txt", sms_text, file_name=f"flood_alert_{real_name}.txt")
        
        # Map
        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup=f"{real_name}: {risk}", icon=folium.Icon(color=color)).add_to(m)
        st_folium(m, width=700, height=400)
        
        st.caption("✅ FloodWatch India - Fully Automatic LIVE System - No Manual Input Needed")

else:
    st.info("👆 Type any city/village name and click Check - App will automatically fetch LIVE rain and give flood alert!")
# ===== FLOOD SMS CODE - PASTE AT BOTTOM =====
import requests

API_KEY = "LlzajuOVkF07M5rfdmBn43w1vhpI62xgKQYSNbyZTDCGsioHeJGexWpqZPNC36uAMzynSL5TXBjg0oth"

def send_sms(number, msg):
    url = "https://www.fast2sms.com/dev/bulkV2"
    r = requests.get(url, params={
        "authorization": API_KEY,
        "route": "q",
        "message": msg,
        "language": "english",
        "numbers": number
    })
    print(r.json())

# TEST - change number to yours
send_sms("8108502124" "86930 38626", "Thane Flood RED ALERT Test - SIH Demo")
# ===== END =====
