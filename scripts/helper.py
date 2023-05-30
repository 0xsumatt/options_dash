import sqlite3

import pandas as pd



def conn_to_db(dbname):
    
    #connect to db
    conn = sqlite3.connect(dbname)
    print(f"connected to {dbname}")
    return conn

    

def read_sqlite_db(db_path, table_name):
    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_path)

    # Create a query string
    query = f'SELECT * FROM {table_name}'

    # Use pandas to execute the query and convert the result into a DataFrame
    df = pd.read_sql_query(query, conn)

    # Convert timestamp from unix to regular time
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Close the connection to the SQLite database
    conn.close()

    return df

