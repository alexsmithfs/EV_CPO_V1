import sys
from pathlib import Path

# Move 3 levels up from this file (source1 -> sources -> python_scripts)
# to set python_scripts as a root search directory
SCRIPT_DIR = Path(__file__).resolve().parent
PYTHON_SCRIPTS_DIR = SCRIPT_DIR.parent.parent
sys.path.append(str(PYTHON_SCRIPTS_DIR))

import pandas as pd
from sqlalchemy import create_engine, text
from utils import generic_loads
from extract import extract_db_new_updated_rev
from transform import transform_rev_src_1

# _____________________________________________________________________________________________
# Pipeline

# _________________________________________________________
# Extract
new_data = extract_db_new_updated_rev("rev_source_1")

# _________________________________________________________
# Transform
transformed_data = transform_rev_src_1(new_data)

# _________________________________________________________
# Load

generic_loads.load_db_rev_staging(transformed_data) # Loading cleaned data to staging table

generic_loads.load_db_rev_clean("rev_source_1_clean") # Loading only new records to clean table

