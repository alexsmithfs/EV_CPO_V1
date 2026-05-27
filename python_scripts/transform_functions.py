# importing for testing only
from extract_functions import extract_db_new_updated_rev

# Imports
import pandas as pd
import numpy as np

# _____________________________________________________________________________________________
# Tranasformation Functions

# _________________________________________________________
# Transformation for rev source 1

def transform_rev_src_1(df):
    # Converting df to DataFrame to use pandas functions
    df = pd.DataFrame(df)

    # Filtering only to transactions that have succeeded or are Pending. We do not want to include failed transactions in our analysis
    df = df[df['transaction_tag'].isin(['Succeeded', 'Pending'])]

    # Update the 'cost' column for 'Pending' transactions as we haven't actually recieved payment yet.
    df.loc[df['transaction_tag'] == 'Pending', 'cost'] = 0

    return df

# _________________________________________________________
# Transformation for rev source 2

def transform_rev_src_2(df):
    # Converting df to DataFrame to use pandas functions
    df = pd.DataFrame(df)

    # Filtering only to transactions that have succeeded or are Pending. We do not want to include failed transactions in our analysis
    df = df[df['transaction_tag'].isin(['Succeeded', 'Pending'])]

    # Update the 'cost' column for 'Pending' transactions as we haven't actually recieved payment yet.
    df.loc[df['transaction_tag'] == 'Pending', 'cost'] = 0

    return df

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

# _________________________________________________________
# Function for transforming revnue sources that have already had the initial cleaning phase done

def transform_rev_data(df):
    # This function will be used to transform the revenue data from all 3 sources in the same way as they have the same structure. We can then call this function in the clean_data_etl_pipeline for all 3 sources instead of having 3 separate transformation functions.
    # Only taking the relevant columns     
    df = df[['transaction_id', 'date_timestamp', 'charger_id', 'cost']]

    # Converting column types
    df = df.astype({
        'transaction_id': 'str',
        'charger_id': 'str',
        'cost': 'float64'  # In pandas/NumPy, 'float64' is the equivalent of a SQL Double
    })

    # Convert the date column to a proper timestamp
    df['date_timestamp'] = pd.to_datetime(df['date_timestamp'])

    return df



# _____________________________________________________________________________________________
# Testing 

if __name__ == "__main__":

    rev_3_df = extract_db_new_updated_rev("rev_source_3_append")
    print(rev_3_df[rev_3_df['transaction_id'] == 'TXN-300374'])
    transformed_rev_3_df = transform_rev_src_3(rev_3_df)
    print(transformed_rev_3_df[transformed_rev_3_df['transaction_id'] == 'TXN-300374'])
    final_rev_3_df = transform_rev_data(transformed_rev_3_df)
    print(final_rev_3_df[final_rev_3_df['transaction_id'] == 'TXN-300374'])
