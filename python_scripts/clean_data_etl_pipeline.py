from extract_functions import extract_db_new_updated_rev
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
def run_pipeline_rev_src_1():
    try:
        clean_data = extract_db_new_updated_rev("rev_source_1_append")
        # add cleaning functions here

    except Exception as e:
        logger.error("Pipeline for Cleaning revenue Source 1 failed!", exc_info=True)
        # add the below line when we have encorporated Spark
        #sys.exit(1)