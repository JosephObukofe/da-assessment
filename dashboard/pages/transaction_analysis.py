import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dashboard.utils.data_loader import load_data
from da_assessment.scripts.config import PROCESSED_TRANSACTION_DATA


def show():
    st.title("Transaction Analysis Dashboard 🚀")
    st.markdown(
        """
        This section provides a detailed analysis of transaction volumes, currency corridors, 
        and growth trends over time. 
        """
    )

    _, transactions_df_copy = load_data(PROCESSED_TRANSACTION_DATA)

    st.subheader("Key Metrics")
    total_transactions = transactions_df_copy.shape[0]
    total_transaction_value = transactions_df_copy["BaseAmount"].sum()

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total_transactions,
            title={"text": "Total Transactions"},
            domain={"x": [0, 0.5], "y": [0, 1]},
        )
    )
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total_transaction_value,
            title={"text": "Total Transaction Value (CAD)"},
            domain={"x": [0.5, 1], "y": [0, 1]},
        )
    )
    st.plotly_chart(fig, use_container_width=False)

    send_currency_volume = (
        transactions_df_copy.groupby("SendCurrencyId")["SendAmount"].sum().reset_index()
    )
    send_currency_volume.columns = ["Send Currency", "Total Volume"]
    send_currency_volume = send_currency_volume.sort_values(
        by="Total Volume",
        ascending=False,
    )

    fig_send_currency = px.bar(
        send_currency_volume,
        x="Send Currency",
        y="Total Volume",
        title="Transaction Volume by Send Currency",
        text_auto=True,
    )
    st.plotly_chart(fig_send_currency)

    currency_corridor_volume = (
        transactions_df_copy.groupby(["SendCurrencyId", "ReceiveCurrencyId"])[
            "SendAmount"
        ]
        .sum()
        .reset_index()
    )
    currency_corridor_volume.columns = [
        "Send Currency",
        "Receive Currency",
        "Total Volume",
    ]
    currency_corridor_volume = currency_corridor_volume.sort_values(
        by="Total Volume",
        ascending=False,
    )

    fig_currency_corridor = px.bar(
        currency_corridor_volume,
        x="Receive Currency",
        y="Total Volume",
        color="Receive Currency",
        title="Transaction Volume by Currency Corridor",
        text_auto=True,
        barmode="relative",
    )
    st.plotly_chart(fig_currency_corridor)

    transactions_df_copy["Transaction Month"] = pd.to_datetime(
        transactions_df_copy["DateCreated"]
    ).dt.to_period("M")
    monthly_corridor_volume = (
        transactions_df_copy.groupby(
            ["Transaction Month", "SendCurrencyId", "ReceiveCurrencyId"]
        )["SendAmount"]
        .sum()
        .reset_index()
    )
    monthly_corridor_volume["Transaction Month"] = monthly_corridor_volume[
        "Transaction Month"
    ].astype(str)
    monthly_corridor_volume["MoMGrowth"] = (
        monthly_corridor_volume.groupby(["SendCurrencyId", "ReceiveCurrencyId"])[
            "SendAmount"
        ].pct_change()
        * 100
    )
    fig_mom_growth = px.line(
        monthly_corridor_volume,
        x="Transaction Month",
        y="MoMGrowth",
        color="SendCurrencyId",
        title="MoM Growth per Corridor",
        markers=True,
    )
    st.plotly_chart(fig_mom_growth)

    with st.expander("Transaction Trends Over Time"):
        transactions_df_copy["Transaction Date"] = pd.to_datetime(
            transactions_df_copy["DateCreated"]
        ).dt.date
        transactions = (
            transactions_df_copy.groupby("Transaction Date")
            .agg({"SendAmount": "sum", "Id": "count"})
            .reset_index()
        )
        transactions.columns = ["Transaction Date", "Total Volume", "Transaction Count"]
        transactions["WoWGrowth"] = (
            transactions["Total Volume"].pct_change(periods=7) * 100
        )
        transactions["MoMGrowth"] = (
            transactions["Total Volume"].pct_change(periods=30) * 100
        )
        fig_trend = px.line(
            transactions,
            x="Transaction Date",
            y="Total Volume",
            title="Transaction Volume Over Time",
            markers=True,
        )
        st.plotly_chart(fig_trend)
        fig_wow_mom = px.line(
            transactions,
            x="Transaction Date",
            y=["WoWGrowth", "MoMGrowth"],
            title="WoW & MoM Growth Trends",
            markers=True,
        )
        st.plotly_chart(fig_wow_mom)

    st.markdown("---")
    st.markdown("*Dashboard powered by Streamlit and Plotly* 😊")
