
import pandas as pd
import httpx
from scripts.helper import read_sqlite_db



def fetch_OI():
    client = httpx.Client()
    response_data = client.get("https://api.aevo.xyz/statistics?asset=ETH&instrument_type=OPTION").json()

    # Extract calls and puts open interest
    calls_open_interest = float(response_data["open_interest"]["calls"])
    puts_open_interest = float(response_data["open_interest"]["puts"])


    # Create a DataFrame with open interest data
    data = {'Type': ['Calls', 'Puts'], 'Open Interest': [calls_open_interest, puts_open_interest]}
    df = pd.DataFrame(data)
    df['Color'] = df['Type'].map({'Calls': 'green', 'Puts': 'red'})
    return df



def fetch_hist_OI():
    df= read_sqlite_db("scripts/aevo_data.db","aevo_data")
    selected_df = df[["timestamp","puts","calls"]]
    
    return selected_df

    
def fetch_put_call():
    df = read_sqlite_db("scripts/aevo_data.db","aevo_data")
    selected_df = df[["timestamp","put_call_ratio"]]
    return selected_df

def fetch_latest_volume():
    df = read_sqlite_db("scripts/aevo_data.db","aevo_data")
    df["name"] = 'Aevo'
    selected_df = df[["name","daily_volume"]]
    latest_volume = selected_df.tail(1)

    return latest_volume

def fetch_latest_prem_volume():
    df = read_sqlite_db("scripts/aevo_data.db","aevo_data")
    df["name"] = 'Aevo'
    selected_df = df[["name","daily_volume_premium"]]
    latest_prem_volume = selected_df.tail(1)

    return latest_prem_volume