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

# Function to load data into SQL database
def load_db(df, table_name):
    df.to_sql(table_name, engine, if_exists='replace', index=False)


# Function to append only new records from the main table to the append table
def load_db_append(table_name):

    table_name_append = f"{table_name}_append"

    # This SQL command does the work internally in Postgres
    sql_command = text(f"""
        INSERT INTO {table_name_append} (
            transaction_id, 
            date_timestamp, 
            charger_id, 
            cost, 
            dwh_date_added
        )
        SELECT 
            t.transaction_id, 
            t.date_timestamp, 
            t.charger_id, 
            t.cost, 
            NOW() AS dwh_date_added
        FROM {table_name} t
        LEFT JOIN {table_name_append} t_append
            ON (t.transaction_id = t_append.transaction_id) AND (t.date_timestamp = t_append.date_timestamp) AND (t.charger_id = t_append.charger_id) AND (t.cost = t_append.cost)
        WHERE t_append.transaction_id IS NULL
        ;
    """)

    # Use engine.begin() to ensure the transaction is committed
    with engine.begin() as connection:
        result = connection.execute(sql_command)
        print(f"Transfer complete. Appended {result.rowcount} new records from {table_name} to {table_name_append}.")


# Testing 
# _____________________________________________________________________________________________

if __name__ == "__main__":

    file_path = R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_3.csv'
    raw_data = pd.read_csv(file_path)

    print(raw_data.info())

    load_db(raw_data, 'rev_source_3')
    load_db_append('rev_source_3') 