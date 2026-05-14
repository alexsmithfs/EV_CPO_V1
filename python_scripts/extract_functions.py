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

# Functions
# _____________________________________________________________________________________________

# Extracting data from csv file
# _________________________________________________________
def extract_csv(file_path):
    raw_data = pd.read_csv(file_path)
    return raw_data

# Extracting ONLY new and updated records for cleaning process
# _________________________________________________________
def extract_csv_new_updated(table_name):

    # This SQL command does the work internally in Postgres
    sql_command = text(f"""
        SELECT 
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            transaction_tag,
            cost_type,
            dwh_date_added,
            dwh_date_updated
        FROM {table_name}
        WHERE (transaction_id, date_timestamp, charger_id) IN (
            SELECT transaction_id, date_timestamp, charger_id
            FROM {table_name}
            EXCEPT
            SELECT transaction_id, date_timestamp, charger_id
            FROM {table_name}_append
        )
        OR (transaction_id, date_timestamp, charger_id) IN (
            SELECT transaction_id, date_timestamp, charger_id
            FROM {table_name}
            INTERSECT
            SELECT transaction_id, date_timestamp, charger_id
            FROM {table_name}_append
        ) AND cost IS DISTINCT FROM (
            SELECT cost 
            FROM {table_name}_append AS append_table
            WHERE append_table.transaction_id = {table_name}.transaction_id 
              AND append_table.date_timestamp = {table_name}.date_timestamp 
              AND append_table.charger_id = {table_name}.charger_id
        );
    """)

    # Use engine.begin() to ensure the transaction is committed
    with engine.begin() as connection:
        result = connection.execute(sql_command)
        new_updated_data = result.fetchall()
        print(f"Extracted {len(new_updated_data)} new and updated records from {table_name} for cleaning process.")
    
    return new_updated_data
