
import streamlit as st
import pandas as pd
import sqlite3
import datetime

# Connect to the SQLite database
conn = sqlite3.connect("wheelsets_demo.db", check_same_thread=False)
cursor = conn.cursor()

def get_wheelset_ids():
    cursor.execute("SELECT Wheelset_ID FROM Wheelset_Master")
    return [row[0] for row in cursor.fetchall()]

def get_asset_data(wheelset_id):
    cursor.execute("SELECT * FROM Wheelset_Master WHERE Wheelset_ID = ?", (wheelset_id,))
    row = cursor.fetchone()
    if row:
        return {
            "Wheelset_ID": row[0],
            "Wagon_No": row[1],
            "Install_Date": row[2],
            "Current_Position": row[3],
            "Total_Mileage": row[4],
            "Current_Condition": row[5],
            "RUL_km": row[6]
        }
    return {}

# UI
st.title("🚆 Freight Wagon Wheelset Tracker")

wheelsets = get_wheelset_ids()
selected_id = st.selectbox("Select Wheelset ID", wheelsets)

asset_data = get_asset_data(selected_id)

if not asset_data:
    st.error("Wheelset not found in database.")
else:
    st.subheader(f"Asset Details - {selected_id}")
    st.markdown(f"**Wheelset ID:** {asset_data['Wheelset_ID']}")
    st.markdown(f"**Wagon No:** {asset_data['Wagon_No']}")
    st.markdown(f"**Install Date:** {asset_data['Install_Date']}")
    st.markdown(f"**Current Position:** {asset_data['Current_Position']}")
    st.markdown(f"**Total Mileage:** {asset_data['Total_Mileage']}")
    st.markdown(f"**Current Condition:** {asset_data['Current_Condition']}")
    st.markdown(f"**Remaining Useful Life (RUL):** {asset_data['RUL_km']} km")
