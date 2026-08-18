import sys
from pathlib import Path

# Move 3 levels up from this file (source1 -> sources -> python_scripts)
# to set python_scripts as a root search directory
SCRIPT_DIR = Path(__file__).resolve().parent
PYTHON_SCRIPTS_DIR = SCRIPT_DIR.parent.parent
sys.path.append(str(PYTHON_SCRIPTS_DIR))

import pandas as pd
from sqlalchemy import create_engine, text
from utils import generic_extracts
from utils import generic_loads

# _____________________________________________________________________________________________
# Pipeline

#file path for revenue source 3
file_path = R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_3.csv'

# Extract
raw_data = generic_extracts.extract_csv(file_path)

# Load
generic_loads.load_raw(raw_data, 'rev_source_3')