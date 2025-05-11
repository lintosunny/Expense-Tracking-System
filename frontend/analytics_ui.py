import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_tab():
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        response = response.json()

        data = {
            "Category": list(response.keys()),
            "Total": [response[category]["total"] for category in response],
            "Percentage": [response[category]["percentage"] for category in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        col = st.columns((1, 1), gap='medium')

        with col[0]:
            st.markdown('#### Expense by category')
            df_sorted_2 = df_sorted.copy()
            df_sorted_2['Percentage'] = df_sorted_2['Percentage'].round(2)
            df_sorted_2['Percentage'] = df_sorted_2['Percentage'].astype(str) + '%'
            df_sorted_2['Total'] = df_sorted_2['Total'].astype(int)
            st.table(df_sorted_2.reset_index(drop=True))


        with col[1]:
            st.markdown('#### ')

            st.dataframe(df_sorted,
                 column_order=("Category", "Percentage"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Category": st.column_config.TextColumn(
                        "Category",
                    ),
                    "Percentage": st.column_config.ProgressColumn(
                        "Percentage",
                        format="%.2f%%",
                        min_value=0,
                        max_value=100,
                     )}
                 )
