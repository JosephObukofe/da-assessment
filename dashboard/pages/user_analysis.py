import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dashboard.utils.data_loader import load_data
from da_assessment.scripts.config import (
    PROCESSED_USER_DATA,
    PROCESSED_TRANSACTION_DATA,
)


def show():
    st.title("User Analytics Dashboard 📈")
    st.markdown(
        """
        This section provides insights into user trends, transaction behaviors, and key growth metrics. 
        Explore trends in user activity, verification rates, transaction volumes, and demographic distributions.
        """
    )

    # Load Data
    _, users_df = load_data(PROCESSED_USER_DATA)
    _, transactions_df = load_data(PROCESSED_TRANSACTION_DATA)

    # Top Metrics Section
    st.subheader("Key Metrics")
    total_users = users_df["Id"].nunique()
    username_counts = users_df.groupby("UserName")["Id"].nunique().reset_index()
    multiple_accounts = username_counts[username_counts["Id"] > 1].shape[0]

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total_users,
            title={"text": "Total Users"},
            domain={"x": [0, 0.5], "y": [0, 1]},
        )
    )
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=multiple_accounts,
            title={"text": "Users with Multiple Accounts"},
            domain={"x": [0.5, 1], "y": [0, 1]},
        )
    )
    st.plotly_chart(fig, use_container_width=False)

    # Two-Column Layout: KYC Trends vs Growth Metrics
    st.subheader("User Verification Trends & Growth Metrics")
    col1, col2 = st.columns(2)

    users_df["DateCreated"] = pd.to_datetime(users_df["DateCreated"], errors="coerce")
    daily_kyc = (
        users_df.groupby([users_df["DateCreated"].dt.date, "IsKYCVerified"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    fig_kyc = px.line(
        daily_kyc,
        x="DateCreated",
        y=[True, False],
        markers=True,
        labels={"value": "Users", "variable": "KYC Status"},
        title="Daily Growth of Verified vs Non-Verified Users",
    )
    col1.plotly_chart(fig_kyc, use_container_width=True)

    daily_kyc["Verified WoW Growth"] = daily_kyc[True].pct_change(periods=7) * 100
    daily_kyc["Non-Verified WoW Growth"] = daily_kyc[False].pct_change(periods=7) * 100

    fig_growth = px.line(
        daily_kyc,
        x="DateCreated",
        y=["Verified WoW Growth", "Non-Verified WoW Growth"],
        markers=True,
        labels={"value": "Growth (%)", "variable": "Growth Type"},
        title="Week-over-Week Growth of Verified Users",
    )
    col2.plotly_chart(fig_growth, use_container_width=True)

    # Expandable Section: Demographics
    with st.expander("User Demographics"):
        st.subheader("Age Distribution")
        users_df["DateOfBirth"] = pd.to_datetime(
            users_df["DateOfBirth"], errors="coerce"
        )
        current_year = datetime.now().year
        users_df["Age"] = current_year - users_df["DateOfBirth"].dt.year
        bins = [0, 17, 25, 35, 45, 55, 65, 100]
        labels = ["<18", "18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
        users_df["AgeGroup"] = pd.cut(
            users_df["Age"], bins=bins, labels=labels, right=True
        )

        age_dist = users_df["AgeGroup"].value_counts().reset_index()
        age_dist.columns = ["AgeGroup", "count"]
        fig_age = px.bar(
            age_dist,
            x="AgeGroup",
            y="count",
            labels={"AgeGroup": "Age Group", "count": "Users"},
            title="User Age Distribution",
        )
        st.plotly_chart(fig_age, use_container_width=True)

        st.subheader("Gender Distribution")
        gender_dist = users_df["Gender"].value_counts().reset_index()
        gender_dist.columns = ["Gender", "count"]
        fig_gender = px.pie(
            gender_dist,
            names="Gender",
            values="count",
            title="Gender Distribution",
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    # Expandable Section: Transaction Insights
    with st.expander("Transaction Insights"):
        st.subheader("Daily Average Transaction Volume per User")
        transactions_df["DateCreated"] = pd.to_datetime(transactions_df["DateCreated"])
        daily_trans = (
            transactions_df.groupby([transactions_df["DateCreated"].dt.date, "UserId"])[
                "BaseAmount"
            ]
            .sum()
            .reset_index()
        )
        daily_avg_vol = (
            daily_trans.groupby("DateCreated")["BaseAmount"].mean().reset_index()
        )
        fig_avg_vol = px.line(
            daily_avg_vol,
            x="DateCreated",
            y="BaseAmount",
            markers=True,
            title="Daily Average Transaction Volume per User",
        )
        st.plotly_chart(fig_avg_vol, use_container_width=True)

    st.markdown("---")
    st.markdown("*Dashboard powered by Streamlit and Plotly* 😊")
