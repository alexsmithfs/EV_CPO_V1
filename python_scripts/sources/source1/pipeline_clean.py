import sys
from pathlib import Path

# Move 3 levels up from this file (source1 -> sources -> python_scripts)
# to set python_scripts as a root search directory
SCRIPT_DIR = Path(__file__).resolve().parent
PYTHON_SCRIPTS_DIR = SCRIPT_DIR.parent.parent
sys.path.append(str(PYTHON_SCRIPTS_DIR))

import pandas as pd
from sqlalchemy import create_engine, text
import logging
from utils import generic_loads
from extract import extract_db_new_updated_rev
from transform import transform_rev_src_1

# Setup Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("etl_pipeline.log"), # Saves errors to a file
        logging.StreamHandler(sys.stdout)        # Also prints to your VSC console
    ]
)
logger = logging.getLogger(__name__)

# _____________________________________________________________________________________________
# Pipeline

def run_pipeline_rev_src_1():
    try:
        # Extracting only new and updated records from rev_source_1_append for cleaning process
        new_data = extract_db_new_updated_rev("rev_source_1")
        # Transforming the new/updated records to clean data
        transformed_data = transform_rev_src_1(new_data)
        # Loading cleaned data to staging table
        generic_loads.load_db_rev_staging(transformed_data)
        # Loading only new records to clean table
        generic_loads.load_db_rev_clean("rev_source_1_clean")

    except Exception as e:
        logger.error("Pipeline for Cleaning revenue Source 1 failed!", exc_info=True)
        # add the below line when we have encorporated Spark
        #sys.exit(1)

# _____________________________________________________________________________________________

if __name__ == "__main__":
    logger.info("Starting ETL Pipeline")
    run_pipeline_rev_src_1()