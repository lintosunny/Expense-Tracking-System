import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "http://localhost:8000"

def monthly_tab():
    response = requests.post(f"{API_URL}/monthly/")
    response = response.json()

    col = st.columns((3, 1), gap='medium')

    with col[0]:

        df = pd.DataFrame(response)

        # Create x-axis labels
        df["month_year"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)

        # Plot with light red color and no edge
        fig, ax = plt.subplots()
        bars = ax.bar(df["month_year"], df["total"], color='#ff9999', edgecolor='none')  # light red, no border

        # Aesthetic adjustments
        ax.set_xlabel("Month")
        ax.set_ylabel("Total")
        ax.set_title("Monthly Expenses")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Display in Streamlit
        st.pyplot(fig)