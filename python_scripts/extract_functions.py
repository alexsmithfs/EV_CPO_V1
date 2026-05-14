import pandas as pd
from sqlalchemy import create_engine, text


# Functions
# _____________________________________________________________________________________________

# Extracting data from csv file
# _________________________________________________________
def extract_csv(file_path):
    raw_data = pd.read_csv(file_path)
    return raw_data

# Extracting ONLY new and updated records from revenue tables in database for cleaning process
# _________________________________________________________
def extract_db_new_updated_rev(table_name):

    db_config = {
    "user": "postgres",
    "password": "Alexsm97",
    "host": "localhost",
    "port": "5432",
    "database": "EV_CPO_DB"
    }

    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    append_table = table_name
    clean_table = append_table.replace("_append", "_clean")

    # This SQL command does the work internally in Postgres
    sql_query = f"""
        SELECT
            r_append.*
        FROM {append_table} r_append

        LEFT JOIN {clean_table} r_clean
            ON r_append.transaction_id = r_clean.transaction_id
            AND r_append.charger_id = r_clean.charger_id
            AND r_append.date_timestamp = r_clean.date_timestamp

        WHERE
            r_clean.transaction_id IS NULL
            OR 
            r_append.cost != r_clean.cost
    """

    rev_data = pd.read_sql_query(sql_query, engine)
    
    return rev_data

if __name__ == "__main__":

    print(extract_db_new_updated_rev("rev_source_1_append"))
