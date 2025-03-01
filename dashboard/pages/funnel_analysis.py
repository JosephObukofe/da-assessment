import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from dashboard.utils.data_loader import load_data
from da_assessment.scripts.config import (
    PROCESSED_USER_DATA,
    PROCESSED_TRANSACTION_DATA,
)


def show():
    st.title("Funnel Analysis")
    st.markdown(
        "This section analyzes user activity across different stages: "
        "**Acquisition → Complete Profile → KYC Verified → Transaction.** "
        "By examining the conversion rates and drop-off points at each stage, "
        "we can identify potential bottlenecks and improve user onboarding processes."
    )

    _, users_df_copy = load_data(PROCESSED_USER_DATA)
    _, transactions_df_copy = load_data(PROCESSED_TRANSACTION_DATA)

    # Funnel Stages
    total_acquired = users_df_copy.shape[0]
    total_completed_profile = users_df_copy[
        users_df_copy["CompletedProfile"] == True
    ].shape[0]
    total_kyc_verified = users_df_copy[users_df_copy["IsKYCVerified"] == True].shape[0]

    # Find users who are KYC Verified & Transacting
    merged_df = transactions_df_copy.merge(
        users_df_copy[["Id", "IsKYCVerified"]],
        left_on="UserId",
        right_on="Id",
        how="inner",
    )

    # Filter only KYC Verified Users who are Transacting
    kyc_verified_transacting_users = merged_df[merged_df["IsKYCVerified"] == True][
        "UserId"
    ].nunique()

    funnel_data = pd.DataFrame(
        {
            "Stage": [
                "Acquisition",
                "Complete Profile",
                "KYC Verified",
                "Transaction",
            ],
            "Users": [
                total_acquired,
                total_completed_profile,
                total_kyc_verified,
                kyc_verified_transacting_users,
            ],
        }
    )

    # Fixing Conversion Rate Calculation
    funnel_data["Conversion Rate"] = (
        funnel_data["Users"].shift(-1) / funnel_data["Users"] * 100
    )
    funnel_data["Drop Off"] = 100 - funnel_data["Conversion Rate"]

    # Handle Edge Cases
    funnel_data["Conversion Rate"] = (
        funnel_data["Conversion Rate"].replace([np.inf, -np.inf], np.nan).fillna(0)
    )
    funnel_data["Drop Off"] = (
        funnel_data["Drop Off"].replace([np.inf, -np.inf], np.nan).fillna(0)
    )

    # Explicitly Set the Last Stage's Drop-Off to 100%
    funnel_data.loc[0, "Drop Off"] = "No drop off"
    funnel_data.loc[len(funnel_data) - 1, "Drop Off"] = 100

    # Funnel Chart
    fig = px.funnel(
        funnel_data,
        x="Users",
        y="Stage",
        title="User Journey Funnel",
    )
    st.plotly_chart(fig)

    # Display Data Table
    st.dataframe(funnel_data)

    # Drop-Off Insights
    for i in range(1, len(funnel_data)):
        drop_off = funnel_data.loc[i, "Drop Off"]
        stage = funnel_data.loc[i, "Stage"]
        st.markdown(f"- **{stage}**: {drop_off:.2f}% drop-off")

    st.markdown("---")
    st.markdown("*Dashboard powered by Streamlit and Plotly* 😊")
