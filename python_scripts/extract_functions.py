import pandas as pd

# Extracting data from csv file
def extract_csv(file_path):
    raw_data = pd.read_csv(file_path)
    return raw_data

