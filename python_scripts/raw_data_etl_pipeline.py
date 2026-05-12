import logging
import sys
from datetime import datetime
from extract_functions import extract_csv
from load_functions import (
    load_db, 
    load_db_rev_src_1_append, 
    load_db_rev_src_2_append, 
    load_db_rev_src_3_append
)

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
        file_path = R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_1.csv'
        logger.info(f"Extracting rev_source_1 from {file_path}")
        raw_data = extract_csv(file_path)
        logger.info(f"Loading rev_source_1 into database")
        load_db(raw_data, 'rev_source_1')
        logger.info(f"Appending rev_source_1 to appended table")
        load_db_rev_src_1_append()

    except Exception as e:
        logger.error("Pipeline for Revenue Source 1 failed!", exc_info=True)
        # add the below line when we have encorporated Spark
        #sys.exit(1)

# rev_source 2 pipeline
def run_pipeline_rev_src_2():
    try:
        file_path = R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_2.csv'
        logger.info(f"Extracting rev_source_2 from {file_path}")
        raw_data = extract_csv(file_path)
        logger.info(f"Loading rev_source_2 into database")
        load_db(raw_data, 'rev_source_2')
        logger.info(f"Appending rev_source_2 to appended table")
        load_db_rev_src_2_append()

    except Exception as e:
        logger.error("Pipeline for Revenue Source 2 failed!", exc_info=True)
        # add the below line when we have encorporated Spark
        #sys.exit(1)

# rev_source 3 pipeline
def run_pipeline_rev_src_3():
    try:
        file_path = R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_3.csv'
        logger.info(f"Extracting rev_source_3 from {file_path}")
        raw_data = extract_csv(file_path)
        logger.info(f"Loading rev_source_3 into database")
        load_db(raw_data, 'rev_source_3')
        logger.info(f"Appending rev_source_3 to appended table")
        load_db_rev_src_3_append()

    except Exception as e:
        logger.error("Pipeline for Revenue Source 3 failed!", exc_info=True)
        # add the below line when we have encorporated Spark
        #sys.exit(1)

if __name__ == "__main__":
    logger.info("Starting ETL Pipeline")
    run_pipeline_rev_src_1()
    run_pipeline_rev_src_2()
    run_pipeline_rev_src_3()
