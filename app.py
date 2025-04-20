import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(layout="wide")
st.markdown("<h1 style='color:#D7263D;'>🚆 Freight Wagon Wheelset Tracker</h1>", unsafe_allow_html=True)

# DB connection
conn = sqlite3.connect("wheelsets_demo.db")
cursor = conn.cursor()

# Fetch Wheelset IDs
wheelset_ids = pd.read_sql("SELECT Wheelset_ID FROM Wheelset_Master", conn)
selected_id = st.selectbox("Select Wheelset ID", wheelset_ids["Wheelset_ID"].tolist())

# Layout
col1, col2 = st.columns([1, 2])

# ========== LEFT SIDE: ASSET SUMMARY ==========
with col1:
    asset_data = pd.read_sql(f"SELECT * FROM Wheelset_Master WHERE Wheelset_ID = '{selected_id}'", conn).iloc[0]

    st.subheader("📄 Asset Summary")
    st.markdown(f"""
    **Wheelset ID:** {asset_data["Wheelset_ID"]}  
    **Wagon No:** {asset_data["Wagon_No"]}  
    **Install Date:** {asset_data["Install_Date"]}  
    **Current Position:** {asset_data["Current_Position"]}  
    **Total Mileage:** {asset_data["Total_Mileage"]} km  
    **Remaining Life:** {asset_data["RUL_km"]} km  
    **Condition:** {asset_data["Current_Condition"]}  
    """)

# ========== RIGHT SIDE: INSPECTION AND MONITORING ==========
with col2:
    st.subheader("🛠️ Inspection Data")
    insp_df = pd.read_sql(f"SELECT * FROM Inspection_Log WHERE Wheelset_ID = '{selected_id}'", conn)
    st.dataframe(insp_df)

    st.subheader("📊 Monitoring Trends")
    mon_df = pd.read_sql(f"SELECT * FROM Monitoring_Data WHERE Wheelset_ID = '{selected_id}'", conn)

    # Flag summary
    alert_flags = mon_df[mon_df["Flag"] == "ALERT"]
    if not alert_flags.empty:
        st.warning("⚠️ Alert flags detected from condition monitoring systems!")

    pivot = mon_df.pivot(index="Date", columns="Metric", values="Value")
    st.bar_chart(pivot)

# ========== ADDITIONAL PAGES ==========
st.subheader("📈 Operational Mileage Logs")
oplog = pd.read_sql(f"SELECT * FROM Wagon_Operational_Log WHERE Wheelset_ID = '{selected_id}'", conn)
st.dataframe(oplog)

st.subheader("🔧 Maintenance History")
mntlog = pd.read_sql(f"SELECT * FROM Maintenance_Log WHERE Wheelset_ID = '{selected_id}'", conn)
st.dataframe(mntlog)

conn.close()
