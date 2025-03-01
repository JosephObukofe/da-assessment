import pandas as pd
import streamlit as st
from da_assessment.scripts.config import (
    PROCESSED_USER_DATA,
    PROCESSED_TRANSACTION_DATA,
)


@st.cache_data
def load_data(file_path):
    """
    Loads the CSV data from the given file path and returns the data and a copy of the data.
    """

    data = pd.read_csv(file_path)
    copy = data.copy()
    return data, copy
