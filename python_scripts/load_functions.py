import pandas as pd
from sqlalchemy import create_engine, text

db_config = {
    "user": "postgres",
    "password": "Alexsm97",
    "host": "localhost",
    "port": "5432",
    "database": "EV_CPO_DB"
}

engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
# _____________________________________________________________________________________________
# Functions 

# _________________________________________________________
# Function to load data into SQL database

def load_db(df, table_name):
    df.to_sql(table_name, engine, if_exists='replace', index=False)

# _________________________________________________________
# Function for table rev_source_1 ONLY to append only new records from the main table to the append table

def load_db_rev_src_1_append():

    table_name = "rev_source_1"

    table_name_append = f"{table_name}_append"

    # This SQL command does the work internally in Postgres
    sql_command = text(f"""
        INSERT INTO {table_name_append} (
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            transaction_tag,
            dwh_date_added,
            dwh_date_updated
        )
        SELECT 
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            transaction_tag,
            NOW(),
            NULL
        FROM {table_name}
        ON CONFLICT (transaction_id, date_timestamp, charger_id) 
        DO UPDATE SET
            cost = EXCLUDED.cost,
            transaction_tag = EXCLUDED.transaction_tag,
            dwh_date_updated = NOW()
        WHERE {table_name_append}.cost IS DISTINCT FROM EXCLUDED.cost;
    """)

    # Use engine.begin() to ensure the transaction is committed
    with engine.begin() as connection:
        result = connection.execute(sql_command)
        print(f"Transfer complete. Appended {result.rowcount} new records from {table_name} to {table_name_append}.")

# _________________________________________________________
# Function for table rev_source_2 ONLY to append only new records from the main table to the append table

def load_db_rev_src_2_append():

    table_name = "rev_source_2"

    table_name_append = f"{table_name}_append"

    # This SQL command does the work internally in Postgres
    sql_command = text(f"""
        INSERT INTO {table_name_append} (
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            transaction_tag,
            dwh_date_added,
            dwh_date_updated
        )
        SELECT 
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            transaction_tag,
            NOW(),
            NULL
        FROM {table_name}
        ON CONFLICT (transaction_id, date_timestamp, charger_id) 
        DO UPDATE SET
            cost = EXCLUDED.cost,
            transaction_tag = EXCLUDED.transaction_tag,
            dwh_date_updated = NOW()
        WHERE {table_name_append}.cost IS DISTINCT FROM EXCLUDED.cost;
    """)

    # Use engine.begin() to ensure the transaction is committed
    with engine.begin() as connection:
        result = connection.execute(sql_command)
        print(f"Transfer complete. Appended {result.rowcount} new records from {table_name} to {table_name_append}.")

# _________________________________________________________
# Function for table rev_source_3 ONLY to append only new records from the main table to the append table

def load_db_rev_src_3_append():

    table_name = "rev_source_3"

    table_name_append = f"{table_name}_append"

    # This SQL command does the work internally in Postgres
    sql_command = text(f"""
        INSERT INTO {table_name_append} (
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            transaction_tag,
            cost_type,
            dwh_date_added,
            dwh_date_updated
        )
        SELECT 
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            transaction_tag,
            cost_type,
            NOW(),
            NULL
        FROM {table_name}
        ON CONFLICT (transaction_id, date_timestamp, charger_id) 
        DO UPDATE SET
            cost = EXCLUDED.cost,
            transaction_tag = EXCLUDED.transaction_tag,
            cost_type = EXCLUDED.cost_type,
            dwh_date_updated = NOW()
        WHERE {table_name_append}.cost IS DISTINCT FROM EXCLUDED.cost
        ;
    """)

    # Use engine.begin() to ensure the transaction is committed
    with engine.begin() as connection:
        result = connection.execute(sql_command)
        print(f"Transfer complete. Appended {result.rowcount} new records from {table_name} to {table_name_append}.")

# _________________________________________________________
# Function to load temporary staging table for revenue data for cleaning process

def load_db_rev_staging(df):

    table_name = "rev_staging"

    df.to_sql(table_name, engine, if_exists='replace', index=False)

# _________________________________________________________
# Function to load clean revenue data into final clean revenue data table, only appending new records and updating exisiting records
# This function can be used for all  revenue sources as the cleaned data will have the same structure regardless of the source

def load_db_rev_clean(table_name):

    staging_table = "rev_staging"

    # This SQL command does the work internally in Postgres
    sql_command = text(f"""
        INSERT INTO {table_name} (
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            dwh_date_added,
            dwh_date_updated
        )
        SELECT 
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            NOW(),
            NULL
        FROM {staging_table}
        ON CONFLICT (transaction_id, date_timestamp, charger_id) 
        DO UPDATE SET
            cost = EXCLUDED.cost,
            dwh_date_updated = NOW()
        WHERE {table_name}.cost IS DISTINCT FROM EXCLUDED.cost;
    """)

    # Use engine.begin() to ensure the transaction is committed
    with engine.begin() as connection:
        result = connection.execute(sql_command)
        print(f"Transfer complete. Appended {result.rowcount} new records from {staging_table} to {table_name}.")

# _____________________________________________________________________________________________
# Testing 

if __name__ == "__main__":

    file_path = R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_3.csv'
    raw_data = pd.read_csv(file_path)

    print(raw_data.info())

    load_db(raw_data, 'rev_source_3')
    load_db_rev_src_3_append()