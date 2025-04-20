
import streamlit as st
import pandas as pd
import sqlite3

# Connect to SQLite
conn = sqlite3.connect("wheelsets_demo.db", check_same_thread=False)
cursor = conn.cursor()

# Title and logo
st.set_page_config(layout="wide", page_title="Freight Wheelset Tracker")
st.markdown("""<h1 style='color:#D7263D;'>🚆 Freight Wagon Wheelset Tracker</h1>"", unsafe_allow_html=True)

# Load wheelset options
wheelset_ids = pd.read_sql("SELECT Wheelset_ID FROM Wheelset_Master", conn)
selected_id = st.selectbox("Select Wheelset ID", wheelset_ids["Wheelset_ID"].tolist())

# Layout
col1, col2 = st.columns([1, 2])

# Fetch and display master data
query = "SELECT * FROM Wheelset_Master WHERE Wheelset_ID = ?"
data = cursor.execute(query, (selected_id,)).fetchone()

if data:
    fields = ["Wheelset_ID", "Wagon_No", "Install_Date", "Current_Position", "Total_Mileage", "Current_Condition", "RUL_km"]
    details = dict(zip(fields, data))

    with col1:
        st.subheader("Asset Summary")
        st.metric("Wheelset ID", details["Wheelset_ID"])
        st.metric("Wagon No", details["Wagon_No"])
        st.metric("Install Date", details["Install_Date"])
        st.metric("Total Mileage", f"{details['Total_Mileage']} km")
        st.metric("Remaining Life", f"{details['RUL_km']} km")
        st.metric("Condition", details["Current_Condition"])

    with col2:
        st.subheader("🛠️ Inspection Data")
        inspection_df = pd.read_sql("SELECT * FROM Inspection_Log WHERE Wheelset_ID = ?", conn, params=(selected_id,))
        st.dataframe(inspection_df)

        st.subheader("📊 Monitoring Trends")
        mon_df = pd.read_sql("SELECT * FROM Monitoring_Data WHERE Wheelset_ID = ?", conn, params=(selected_id,))
        st.bar_chart(mon_df.pivot(index="Date", columns="Metric", values="Value"))

else:
    st.error("Wheelset not found.")
