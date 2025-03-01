import numpy as np
import pandas as pd
from dashboard.utils.data_loader import load_data
from da_assessment.scripts.config import (
    UNPROCESSED_USER_DATA,
    UNPROCESSED_TRANSACTION_DATA,
    PROCESSED_USER_DATA,
    PROCESSED_TRANSACTION_DATA,
)


# Data Loading
_, user_df_copy = load_data(UNPROCESSED_USER_DATA)
_, transaction_df_copy = load_data(UNPROCESSED_TRANSACTION_DATA)


# User Table Preprocessing
# Dropping specified columns from the dataframe ("ReferralCode" and "ReferredBy")
user_df_copy.drop(columns=["ReferralCode", "ReferredBy"], inplace=True)


# Convert columns to specified data types
user_df_copy["Gender"] = user_df_copy["Gender"].astype("category")
user_df_copy["ResidenceCountry"] = user_df_copy["ResidenceCountry"].astype("category")
user_df_copy["KycStatus"] = user_df_copy["KycStatus"].astype("int16")
user_df_copy["State"] = user_df_copy["State"].astype("category")


# Standardizing the "State" column values
def standardize_state(column: str) -> str:
    """Standardizes the 'State' column values"""

    if pd.isna(column) or column.strip() == "":
        return "Unspecified"

    column = column.strip().lower()

    if column in ["abuja", "fct"]:
        return "Federal Capital Territory"

    if "state" not in column:
        return column.capitalize() + " State"

    return column.replace("state", "State").title()


# Standardizing the "Occupation" column values
def standardize_occupation(column: str) -> str:
    """Standardizes the 'Occupation' column values"""

    if pd.isna(column) or column.strip() == "":
        return "Unspecified"

    return column.strip().title()


user_df_copy["State"] = user_df_copy["State"].map(standardize_state)
user_df_copy["Occupation"] = user_df_copy["Occupation"].map(standardize_occupation)


# Transactions Table Preprocessing
# Convert columns to specified data types
transaction_df_copy["Id"] = transaction_df_copy["Id"].astype("object")


# Remove nulls from the "UserId" column
transaction_df_copy = transaction_df_copy.dropna(subset=["UserId"])


# Replacing nulls with "Unspecified" in the "Narration" column
transaction_df_copy["Narration"] = transaction_df_copy["Narration"].fillna(
    "Unspecified"
)


# Save the processed DataFrames as CSV files
user_df_copy.to_csv(PROCESSED_USER_DATA, index=False)
transaction_df_copy.to_csv(PROCESSED_TRANSACTION_DATA, index=False)

print(f"Processed user data saved to: {PROCESSED_USER_DATA}")
print(f"Processed transaction data saved to: {PROCESSED_TRANSACTION_DATA}")
