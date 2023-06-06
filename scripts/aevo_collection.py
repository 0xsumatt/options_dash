import httpx

import time
from datetime import datetime, timedelta

from helper import conn_to_db


def get_data():
    client = httpx.Client()
    req = client.get(
        url="https://api.aevo.xyz/statistics?asset=ETH&instrument_type=OPTION"
    ).json()

    conn = conn_to_db("aevo_data.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS aevo_data (
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
                )"""
    )

    asset = req["asset"]
    ts = int(time.time())
    calls = req["open_interest"]["calls"]
    puts = req["open_interest"]["puts"]
    total = req["open_interest"]["total"]
    index_price = req["index_price"]
    index_daily_change = req["index_daily_change"]
    daily_volume = req["daily_volume"]
    put_call_ratio = req["put_call_ratio"]
    c.execute(
        """INSERT INTO aevo_data (timestamp,asset, calls, puts, total, index_price, index_daily_change, daily_volume, put_call_ratio)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            ts,
            asset,
            calls,
            puts,
            total,
            index_price,
            index_daily_change,
            daily_volume,
            put_call_ratio,
        ),
    )

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

    print(f"function called at {datetime.now()} ")


if __name__ == "__main__":
    
    # Call the function
    get_data()
