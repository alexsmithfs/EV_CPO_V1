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
            NOW() ASdwh_date_added,
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