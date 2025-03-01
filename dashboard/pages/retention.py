import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from dashboard.utils.data_loader import load_data
from da_assessment.scripts.config import (
    PROCESSED_TRANSACTION_DATA,
)


def show():
    st.title("Retention Analysis Dashboard 🔁")
    st.markdown(
        """
        This section provides insights into user retention by tracking active users over time. 
        We analyze **Weekly & Monthly Active Users**, **User Segmentation by Transaction Volume**, 
        and **Daily, Weekly, and Monthly Trends** to measure user engagement and retention.
        """
    )

    _, transactions_df_copy = load_data(PROCESSED_TRANSACTION_DATA)

    # Convert DateCreated column to datetime
    transactions_df_copy["DateCreated"] = pd.to_datetime(
        transactions_df_copy["DateCreated"]
    )

    # Extract week and month timestamps for grouping
    transactions_df_copy["TransactionWeek"] = (
        transactions_df_copy["DateCreated"].dt.to_period("W").dt.to_timestamp()
    )
    transactions_df_copy["TransactionMonth"] = (
        transactions_df_copy["DateCreated"].dt.to_period("M").dt.to_timestamp()
    )

    # Weekly and Monthly Active Users
    weekly_active_users = (
        transactions_df_copy.groupby("TransactionWeek")["UserId"]
        .nunique()
        .reset_index()
    )
    monthly_active_users = (
        transactions_df_copy.groupby("TransactionMonth")["UserId"]
        .nunique()
        .reset_index()
    )

    # Plot Weekly Active Users
    fig_weekly = px.line(
        weekly_active_users,
        x="TransactionWeek",
        y="UserId",
        title="Weekly Active Users Trend",
        markers=True,
        labels={"UserId": "Active Users", "TransactionWeek": "Week"},
    )
    st.plotly_chart(fig_weekly, use_container_width=True)

    # Plot Monthly Active Users
    fig_monthly = px.line(
        monthly_active_users,
        x="TransactionMonth",
        y="UserId",
        title="Monthly Active Users Trend",
        markers=True,
        labels={"UserId": "Active Users", "TransactionMonth": "Month"},
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    # User Segmentation by Transaction Volume
    user_transaction_counts = (
        transactions_df_copy.groupby("UserId")
        .size()
        .reset_index(name="TransactionCount")
    )
    user_transaction_counts["Category"] = pd.cut(
        user_transaction_counts["TransactionCount"],
        bins=[0, 3, 5, 10, 20, float("inf")],
        labels=["1-3", "4-5", "6-10", "11-20", "20+"],
    )
    user_transaction_distribution = (
        user_transaction_counts["Category"].value_counts().reset_index()
    )
    user_transaction_distribution.columns = [
        "Transaction Volume Category",
        "User Count",
    ]

    # Plot User Segmentation
    fig_category = px.bar(
        user_transaction_distribution,
        x="Transaction Volume Category",
        y="User Count",
        text="User Count",
        title="User Segmentation by Transaction Volume",
        labels={
            "Transaction Volume Category": "Transaction Volume",
            "User Count": "User Count",
        },
        color="Transaction Volume Category",
    )
    st.plotly_chart(fig_category, use_container_width=True)

    # Daily, Weekly, and Monthly Insights
    daily_transactions = (
        transactions_df_copy.groupby(transactions_df_copy["DateCreated"].dt.date)[
            "UserId"
        ]
        .nunique()
        .reset_index()
    )
    weekly_transactions = (
        transactions_df_copy.groupby("TransactionWeek")["UserId"]
        .nunique()
        .reset_index()
    )
    monthly_transactions = (
        transactions_df_copy.groupby("TransactionMonth")["UserId"]
        .nunique()
        .reset_index()
    )

    daily_transactions.columns = ["Date", "Active Users"]
    weekly_transactions.columns = ["Week", "Active Users"]
    monthly_transactions.columns = ["Month", "Active Users"]

    # Plot Daily Active Users
    fig_daily = px.line(
        daily_transactions,
        x="Date",
        y="Active Users",
        title="Daily Active Users Trend",
        markers=True,
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # Plot Weekly Active Users Count
    fig_weekly_detailed = px.bar(
        weekly_transactions,
        x="Week",
        y="Active Users",
        text="Active Users",
        title="Weekly Active Users Count",
    )
    st.plotly_chart(fig_weekly_detailed, use_container_width=True)

    # Plot Monthly Active Users Count
    fig_monthly_detailed = px.bar(
        monthly_transactions,
        x="Month",
        y="Active Users",
        text="Active Users",
        title="Monthly Active Users Count",
    )
    st.plotly_chart(fig_monthly_detailed, use_container_width=True)

    st.markdown("---")
    st.markdown("*Dashboard powered by Streamlit and Plotly* 😊")
