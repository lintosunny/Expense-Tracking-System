import streamlit as st
from manage_ui import manage_tab
from analytics_ui import analytics_tab

st.title("Expense Management System")

tab1, tab2 = st.tabs(["Manage", "Analytics"])

with tab1:
    manage_tab()

with tab2:
    analytics_tab()