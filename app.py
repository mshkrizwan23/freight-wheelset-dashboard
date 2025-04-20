import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")
st.markdown("<h1 style='color:#D7263D;'>🚆 Freight Wagon Wheelset Tracker</h1>", unsafe_allow_html=True)

conn = sqlite3.connect('wheelsets_demo.db')
wheelset_ids = pd.read_sql("SELECT DISTINCT Wheelset_ID FROM Wheelset_Master", conn)["Wheelset_ID"].tolist()
selected_id = st.selectbox("Select Wheelset ID", wheelset_ids)