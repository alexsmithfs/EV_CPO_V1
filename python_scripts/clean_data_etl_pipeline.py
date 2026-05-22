from extract_functions import extract_db_new_updated_rev
from transform_functions import transform_rev_src_1, transform_rev_data
from load_functions import load_db_rev_staging, load_db_rev_clean
import logging
import sys


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

# rev_source 1 pipeline
# _____________________________________________________________________________________________

def run_pipeline_rev_src_1():
    try:
        # Extracting only new and updated records from rev_source_1_append for cleaning process
        new_data = extract_db_new_updated_rev("rev_source_1_append")
        # Transforming the new/updated records to clean data
        transformed_data = transform_rev_src_1(new_data)
        cleaned_data = transform_rev_data(transformed_data)
        # Loading cleaned data to staging table
        load_db_rev_staging(cleaned_data)
        # Loading only new records to clean table
        load_db_rev_clean("rev_source_1_clean")

    except Exception as e:
        logger.error("Pipeline for Cleaning revenue Source 1 failed!", exc_info=True)
        # add the below line when we have encorporated Spark
        #sys.exit(1)

run_pipeline_rev_src_1()