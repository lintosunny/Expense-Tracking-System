import streamlit as st
from manage_ui import manage_tab
from analytics_ui import analytics_tab
from monthly_ui import monthly_tab

st.title("💸 Expense Management System")

tab1, tab2, tab3 = st.tabs(["Manage", "Analytics", "Monthly"])

with tab1:
    manage_tab()

with tab2:
    analytics_tab()

with tab3:
    monthly_tab()