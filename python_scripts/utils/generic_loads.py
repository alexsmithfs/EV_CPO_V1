
import pandas as pd
from sqlalchemy import create_engine, text

def load_raw(df, table_name):
    db_config = {
    "user": "postgres",
    "password": "Alexsm97",
    "host": "localhost",
    "port": "5432",
    "database": "EV_CPO_DB"
    }
    
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw_bronze",
        if_exists="replace",  # Use 'replace' to drop and recreate, or 'append'
        index=False
    )