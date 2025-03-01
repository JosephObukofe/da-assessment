import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from dashboard.utils.data_loader import load_data
from da_assessment.scripts.config import (
    PROCESSED_USER_DATA,
)


def show():
    st.title("KYC Status Dashboard 🔍")
    st.markdown(
        """
    This section provides a comprehensive analysis of **Know Your Customer (KYC) status** 
    across users. KYC verification is a crucial step in ensuring compliance, reducing 
    fraud, and improving platform security.  

    We analyze how users progress through different KYC stages, from **Not Started** to 
    **Pending, Passed, In Review, and Failed**. By tracking these statuses over time, 
    we can identify trends, monitor onboarding efficiency, and pinpoint potential 
    bottlenecks in the verification process.  

    The visualizations below offer a clear breakdown of KYC status distribution and how 
    these statuses evolve, helping to improve compliance strategies and user engagement.
    """
    )

    _, users_df_copy = load_data(PROCESSED_USER_DATA)

    kyc_mapping = {
        1: "Not Started",
        2: "Pending",
        3: "Passed",
        4: "In Review",
        5: "Unspecified",
        6: "Failed",
    }

    users_df_copy["KYCStatusMapped"] = users_df_copy["KycStatus"].map(kyc_mapping)
    users_df_copy["DateCreated"] = pd.to_datetime(users_df_copy["DateCreated"])

    # KYC Status Distribution (Sorted from Highest to Lowest)
    kyc_counts = users_df_copy["KYCStatusMapped"].value_counts().reset_index()
    kyc_counts.columns = ["KYC Status", "User Count"]
    kyc_counts = kyc_counts.sort_values(by="User Count", ascending=False)

    fig_count = px.bar(
        kyc_counts,
        x="KYC Status",
        y="User Count",
        title="KYC Status Distribution",
        color="KYC Status",
        text_auto=True,
    )
    st.plotly_chart(fig_count)

    # KYC Trend Over Time
    users_df_copy["DateOnly"] = users_df_copy["DateCreated"].dt.date
    kyc_trend = (
        users_df_copy.groupby(["DateOnly", "KYCStatusMapped"])
        .size()
        .reset_index(name="Count")
    )

    fig_trend = px.line(
        kyc_trend,
        x="DateOnly",
        y="Count",
        color="KYCStatusMapped",
        title="KYC Status Trends Over Time",
    )
    st.plotly_chart(fig_trend)

    st.markdown("---")
    st.markdown("*Dashboard powered by Streamlit and Plotly* 😊")
