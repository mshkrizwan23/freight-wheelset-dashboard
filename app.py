
import streamlit as st
import pandas as pd
import sqlite3
import datetime

st.set_page_config(page_title="Freight Wheelset Dashboard", layout="wide")

st.title("🚆 Freight Wagon Wheelset Tracker")

# Connect to the SQLite database
conn = sqlite3.connect("wheelsets_demo.db", check_same_thread=False)
cursor = conn.cursor()

# Load wheelset IDs
wheelsets = pd.read_sql("SELECT Wheelset_ID FROM Wheelset_Master", conn)
wheelset_ids = wheelsets["Wheelset_ID"].tolist()

# Select a wheelset
selected_id = st.selectbox("Select Wheelset ID", wheelset_ids)

# Fetch and show asset details
asset_query = f"SELECT * FROM Wheelset_Master WHERE Wheelset_ID = '{selected_id}'"
asset_data = pd.read_sql(asset_query, conn).iloc[0]

st.subheader(f"Asset Details - {selected_id}")
st.markdown("""
**Wheelset ID**: {}  
**Wagon No**: {}  
**Install Date**: {}  
**Current Position**: {}  
**Total Mileage**: {}  
**Current Condition**: {}  
**Remaining Useful Life (RUL)**: {} km  
""").format(
    asset_data["Wheelset_ID"],
    asset_data["Wagon_No"],
    asset_data["Install_Date"],
    asset_data["Current_Position"],
    asset_data["Total_Mileage"],
    asset_data["Current_Condition"],
    asset_data["RUL_km"]
)

# Inspection Log Section
st.subheader("📋 Wheelset Inspection Log")
try:
    inspections = pd.read_sql(f"SELECT * FROM Inspection_Log WHERE Wheelset_ID = '{selected_id}'", conn)
    if inspections.empty:
        st.info("No inspection records available.")
    else:
        st.dataframe(inspections)
except Exception as e:
    st.error(f"Error loading inspection logs: {e}")

# Monitoring Data Section
st.subheader("📡 Condition Monitoring Data")
try:
    monitoring = pd.read_sql(f"SELECT * FROM Monitoring_Data WHERE Wheelset_ID = '{selected_id}'", conn)
    if monitoring.empty:
        st.info("No monitoring data available.")
    else:
        for metric in monitoring["Metric"].unique():
            subset = monitoring[monitoring["Metric"] == metric]
            st.markdown(f"**{metric}**")
            st.line_chart(subset.set_index("Date")["Value"])
except Exception as e:
    st.error(f"Error loading monitoring data: {e}")

conn.close()
