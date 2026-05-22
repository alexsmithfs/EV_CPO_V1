# importing for testing only
from extract_functions import extract_db_new_updated_rev

# Imports
import pandas as pd

# Tranasformation Functions
# _____________________________________________________________________________________________


# Transformation for rev source 1
# _________________________________________________________

def transform_rev_src_1(df):
        # Converting df to DataFrame to use pandas functions
        df = pd.DataFrame(df)

        # Filtering only to transactions that have succeeded or are Pending. We do not want to include failed transactions in our analysis
        df = df[df['transaction_tag'].isin(['Succeeded', 'Pending'])]

        # Update the 'cost' column for 'Pending' transactions as we haven't actually recieved payment yet.
        df.loc[df['transaction_tag'] == 'Pending', 'cost'] = 0

        return df

# Generic transform function for revenue data
# _________________________________________________________

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



# Testing 
# _____________________________________________________________________________________________

if __name__ == "__main__":

    rev_1_df = extract_db_new_updated_rev("rev_source_1_append")
    print(rev_1_df[rev_1_df['transaction_tag'] == 'Pending'].head())
    transformed_rev_1_df = transform_rev_src_1(rev_1_df)
    print(transformed_rev_1_df[transformed_rev_1_df['transaction_tag'] == 'Pending'].head())
    final_rev_1_df = transform_rev_data(transformed_rev_1_df)
    print(final_rev_1_df[final_rev_1_df['transaction_id'] == 'TXN-100279'])
