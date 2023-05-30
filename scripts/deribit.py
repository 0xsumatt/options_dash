import httpx
import polars as pl
import time
from helper import conn_to_db

client = httpx.Client()

# log time 
time_of_req= time.time()
req = client.get("https://www.deribit.com/api/v2/public/get_trade_volumes?extended=true").json()['result']


def deribit_volume_df():
   

    req_df = pl.DataFrame(req)
    client.close()
    df_filter = req_df.filter(
        (~req_df['currency'].str.contains('USDC')) &
        (~req_df['currency'].str.contains('ETHW')) &
        (~req_df['currency'].str.contains('SOL'))
    )
    refined_df = df_filter.select(['currency','puts_volume_7d','puts_volume_30d','puts_volume','calls_volume_7d','calls_volume_30d','calls_volume'])
    complete_df = refined_df.with_columns([
        (pl.col("puts_volume")+pl.col("calls_volume")).alias("Cumulative 24H Volume"),
        (pl.col("puts_volume_7d")+pl.col("calls_volume_7d")).alias("Cumulative 7D Volume"),
        (pl.col("puts_volume_30d")+pl.col("calls_volume_30d")).alias("Cumulative 30D Volume"),
    ])



    return {'complete_df':complete_df,'time_of_req':time_of_req}
    
    
    #function to log data to db for later use

def log_deribit_data(df_dict):
    conn = conn_to_db("deribit.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS deribit_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp INTEGER,
                        asset TEXT,
                        calls REAL,
                        puts REAL,
                        total REAL,
                        index_price REAL,
                        index_daily_change REAL,
                        daily_volume REAL,
                        put_call_ratio REAL
                    )''')

    for i, row in df_dict['complete_df'].iterrows():
        asset = row['currency']
        ts = df_dict['time_of_req']
        calls = row['calls_volume']
        puts = row['puts_volume']
        total = row['Cumulative 24H Volume']
        index_price = None  # replace with actual index price if available
        index_daily_change = None  # replace with actual index daily change if available
        daily_volume = row['Cumulative 24H Volume']
        put_call_ratio = puts / calls

        c.execute('''INSERT INTO deribit_data (timestamp, asset, calls, puts, total, index_price, index_daily_change, daily_volume, put_call_ratio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (ts, asset, calls, puts, total, index_price, index_daily_change, daily_volume, put_call_ratio))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    task = deribit_volume_df()
    logger = log_deribit_data(task)