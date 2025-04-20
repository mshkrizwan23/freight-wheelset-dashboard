import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

st.set_page_config(layout="wide")

# Title
st.markdown("<h1 style='color:#D7263D;'>🚆 Freight Wagon Wheelset Tracker</h1>", unsafe_allow_html=True)

# Load database
conn = sqlite3.connect("wheelsets_demo.db")
cursor = conn.cursor()

# Load Wheelset IDs
wheelset_ids = pd.read_sql("SELECT DISTINCT Wheelset_ID FROM Wheelset_Master", conn)["Wheelset_ID"].tolist()
wheelset_id = st.selectbox("Select Wheelset ID", wheelset_ids)

# Asset Info
asset_query = f"SELECT * FROM Wheelset_Master WHERE Wheelset_ID = '{wheelset_id}'"
asset_info = pd.read_sql(asset_query, conn).iloc[0]

# Inspection Info
insp_query = f"SELECT * FROM Inspection_Data WHERE Wheelset_ID = '{wheelset_id}'"
inspection_data = pd.read_sql(insp_query, conn)

# Monitoring Flags
monitoring_df = pd.read_csv("monitoring_flags.csv")
flags_for_wheelset = monitoring_df[monitoring_df["Wheelset_ID"] == wheelset_id]

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🗂️ Asset Summary")
    st.write(f"**Wheelset ID:** {asset_info['Wheelset_ID']}")
    st.write(f"**Wagon No:** {asset_info['Wagon_No']}")
    st.write(f"**Install Date:** {asset_info['Install_Date']}")
    st.write(f"**Current Position:** {asset_info['Position']}")
    st.write(f"**Total Mileage:** {asset_info['Mileage']} km")
    st.write(f"**Remaining Life:** {asset_info['Remaining_Life']} km")
    st.write(f"**Condition:** {asset_info['Condition']}")

with col2:
    st.markdown("### 🛠️ Inspection Data")
    st.dataframe(inspection_data)

# Monitoring flags
st.markdown("### 📊 Monitoring Trends")
if not flags_for_wheelset.empty:
    st.dataframe(flags_for_wheelset)
    for system in ["WILD", "ECM", "HABD"]:
        sys_flag = flags_for_wheelset[flags_for_wheelset["System"] == system]
        if not sys_flag.empty:
            latest = sys_flag.sort_values("Date", ascending=False).iloc[0]
            if latest["Flag"] == "ALERT":
                st.error(f"🚨 {system} ALERT: {latest['Comment']}")
            elif latest["Flag"] == "INFO":
                st.warning(f"⚠️ {system} Info: {latest['Comment']}")
else:
    st.success("✅ No alerts or warnings found.")