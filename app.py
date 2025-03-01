import streamlit as st
import time
from dashboard.pages import (
    user_analysis,
    kyc_status,
    transaction_analysis,
    retention,
    funnel_analysis,
)

# Page Config
st.set_page_config(
    page_title="User & Transaction Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
custom_css = """
<style>
    .css-18e3th9 {
        background-color: #f8f9fa !important;
    }
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(to right, #007bff, #6610f2);
        color: white;
        font-weight: bold;
    }
    .stMetric {
        background: #ffffff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.selectbox(
    "Select a Page",
    [
        "User Analysis",
        "KYC Status Analysis",
        "Transaction Analysis",
        "Retention Analysis",
        "Funnel Analysis",
    ],
)


# Auto refresh
def auto_refresh(interval=5):
    """Refreshes the app at a set interval"""
    st.sidebar.markdown("🔄 **Auto Refresh**")
    refresh = st.sidebar.button(f"Refresh Now ⏳ ({interval}s)")
    if refresh:
        time.sleep(interval)
        st.rerun()


# Page rendering
if page == "User Analysis":
    st.sidebar.success("Analyzing Users 📈")
    auto_refresh(interval=10)
    user_analysis.show()

elif page == "KYC Status Analysis":
    st.sidebar.success("KYC Verification Insights 🔍")
    auto_refresh(interval=15)
    kyc_status.show()

elif page == "Transaction Analysis":
    st.sidebar.success("Exploring Transactions 💰")
    auto_refresh(interval=10)
    transaction_analysis.show()

elif page == "Retention Analysis":
    st.sidebar.success("User Retention Metrics 🔄")
    auto_refresh(interval=12)
    retention.show()

elif page == "Funnel Analysis":
    st.sidebar.success("Funnel Conversion Insights 📊")
    auto_refresh(interval=10)
    funnel_analysis.show()


# --- CONTACT & GITHUB LINKS ---
st.sidebar.markdown("---")
st.sidebar.markdown("💻 **More Info:**")
st.sidebar.markdown("[GitHub Repo](https://github.com/JosephObukofe) 🔗")
st.sidebar.markdown("[Email Support](mailto:josephobukofe@gmail.com) 📧")
