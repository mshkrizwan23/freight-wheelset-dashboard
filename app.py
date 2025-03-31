import streamlit as st
import pandas as pd
import sqlite3
import datetime

# Connect to the SQLite database
conn = sqlite3.connect("wheelsets_demo.db", check_same_thread=False)
cursor = conn.cursor()

# Load wheelset IDs
def get_wheelset_ids():
    query = "SELECT Wheelset_ID FROM Wheelset_Master"
    return [row[0] for row in cursor.execute(query).fetchall()]

# Show wheelset details
def show_wheelset_details(wheelset_id):
    st.subheader(f"Asset Details - {wheelset_id}")
    ws_query = f"SELECT * FROM Wheelset_Master WHERE Wheelset_ID = ?"
    ws_data = cursor.execute(ws_query, (wheelset_id,)).fetchone()
    if ws_data:
        labels = ["Wheelset_ID", "Wagon_No", "Install_Date", "Current_Position", "Total_Mileage", "Current_Condition", "RUL_km"]
        for label, value in zip(labels, ws_data):
            st.write(f"**{label.replace('_', ' ')}**: {value}")

        st.subheader("📋 Inspection History")
        df = pd.read_sql_query("SELECT * FROM Inspection_Log WHERE Wheelset_ID = ?", conn, params=(wheelset_id,))
        st.dataframe(df)

        st.subheader("📈 Monitoring Data")
        df2 = pd.read_sql_query("SELECT * FROM Monitoring_Data WHERE Wheelset_ID = ?", conn, params=(wheelset_id,))
        st.dataframe(df2)
    else:
        st.error("Wheelset not found in database.")

# UI
st.title("🚆 Freight Wagon Wheelset Tracker")

wheelsets = get_wheelset_ids()
selected = st.selectbox("Select Wheelset ID", wheelsets)

if selected:
    show_wheelset_details(selected)
