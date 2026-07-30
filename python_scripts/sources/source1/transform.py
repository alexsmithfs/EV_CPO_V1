
# Imports
import pandas as pd
import numpy as np


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