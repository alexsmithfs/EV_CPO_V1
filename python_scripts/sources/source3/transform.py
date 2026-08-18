# Imports
import pandas as pd
import numpy as np


# _________________________________________________________
# Transformation for rev source 3

def transform_rev_src_3(df):
    # Converting df to DataFrame to use pandas functions
    df = pd.DataFrame(df)

    # Filtering only to transactions that have succeeded or are Pending. We do not want to include failed transactions in our analysis
    df = df[df['transaction_tag'].isin(['Succeeded', 'Pending', 'Refunded'])]

    # Update the 'cost' column for 'Pending' transactions as we haven't actually recieved payment yet.
    df.loc[df['transaction_tag'] == 'Pending', 'cost'] = 0

    # If 'cost_type' is REFUND, multiply by -1, otherwise multiply by 1
    df["net_cost"] = df["cost"] * np.where(df["cost_type"] == "REFUND", -1, 1)
    
    # Group and sum
    cleaned_df = (
        df.groupby(["transaction_id", "charger_id"], as_index=False)
        .agg(
            cost=("net_cost", "sum"),
            date_timestamp=("date_timestamp", "min"),  # Get the latest timestamp for each transaction_id and charger_id
        )
    )
    
    return cleaned_df