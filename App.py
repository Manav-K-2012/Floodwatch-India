import streamlit as st
   import pandas as pd
   import pickle

   st.set_page_config(page_title="FloodWatch India", layout="wide")
   st.title("🌊 FloodWatch India")
   st.write("Real-time flood monitoring dashboard")

   # Load model if it exists
   try:
       model = pickle.load(open('flood_model.pkl', 'rb'))
       st.success("Model loaded!")
   except:
       st.warning("flood_model.pkl not found yet")

   st.button("Check Flood Risk")
