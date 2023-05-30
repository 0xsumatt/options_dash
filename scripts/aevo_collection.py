import httpx

import time
from datetime import datetime,timedelta

from helper import conn_to_db

def get_data():
    client = httpx.Client()
    req = client.get(url = "https://api.aevo.xyz/statistics?asset=ETH&instrument_type=OPTION").json()


    conn = conn_to_db("aevo_data.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS aevo_data (
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

    asset = req["asset"]
    ts = int(time.time())
    calls = req["open_interest"]["calls"]
    puts = req["open_interest"]["puts"]
    total = req["open_interest"]["total"]
    index_price = req["index_price"]
    index_daily_change = req["index_daily_change"]
    daily_volume = req["daily_volume"]
    put_call_ratio = req["put_call_ratio"]
    c.execute('''INSERT INTO aevo_data (timestamp,asset, calls, puts, total, index_price, index_daily_change, daily_volume, put_call_ratio)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (ts,asset, calls, puts, total, index_price, index_daily_change, daily_volume,put_call_ratio))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

    print(f"function called at {datetime.now()} ")
    


if __name__ == '__main__':
    current_time = datetime.utcnow()

    # Calculate the timestamp for 11:59:55 PM UTC today
    target_datetime = datetime.utcnow().replace(hour=23, minute=59, second=56, microsecond=0)

    # If the target time is in the past, add one day to the target time
    if target_datetime.timestamp() <= current_time.timestamp():
        target_datetime += timedelta(days=1)

    # Calculate the number of seconds until the target time
    sleep_time = (target_datetime - datetime.utcnow()).total_seconds()
    print(sleep_time)
    # Wait until the target time
    time.sleep(sleep_time)

    
    # Call the function
    get_data()