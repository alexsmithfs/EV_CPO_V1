import pandas as pd
from sqlalchemy import create_engine

db_config = {
    "user": "postgres",
    "password": "Alexsm97",
    "host": "localhost",
    "port": "5432",
    "database": "EV_CPO_DB"
}

engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

def load_db(df, table_name):
    df.to_sql(table_name, engine, if_exists='replace', index=False)


def load_db_append(table_name, table_name_append):

    # Using SQL query to dynimcally append only new records from the main table to the append table
    sql_query = f'''
        SELECT 
            t.transaction_id, 
            t.date_timestamp, 
            t.charger_id, 
            t.cost, 
            NOW() AS dwh_date_added
        FROM {table_name} t
        LEFT JOIN {table_name_append} t_append
            ON (t.transaction_id = t_append.transaction_id) AND (t.date_timestamp = t_append.date_timestamp) AND (t.charger_id = t_append.charger_id) AND (t.cost = t_append.cost)
        WHERE t_append.transaction_id IS NULL;
    '''
    df = pd.read_sql(sql_query, engine)
    df.to_sql(table_name_append, engine, if_exists='append', index=False)


file_path = R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_3.csv'
raw_data = pd.read_csv(file_path)

print(raw_data.info())

load_db(raw_data, 'rev_source_3')
load_db_append('rev_source_3', 'rev_source_3_append')    