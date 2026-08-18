import pandas as pd

# _____________________________________________________________________________________________
# Functions

# _________________________________________________________
# Extracting data from csv file
def extract_csv(file_path):
    raw_data = pd.read_csv(file_path)
    return raw_data