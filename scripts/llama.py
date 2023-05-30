import httpx

import pandas as pd



def get_llama_prem_vol_data():
    try:
        client = httpx.Client()
        #get data from defi llama for lyra,premia and thales
        req = client.get("https://api.llama.fi/overview/options?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=false&dataType=dailyPremiumVolume").json()['protocols']
        df = pd.DataFrame(req)
        refine_df = df[["name","total24h","total7d","total30d","totalAllTime"]]
        client.close()
        return refine_df
    except Exception as e:
        print("unable to get data",e)

def get_llama_vol_data():
    try:
        client = httpx.Client()
        req = client.get("https://api.llama.fi/overview/options?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=false").json()['protocols']
        df = pd.DataFrame(req)
        refined_df = df[['name','total24h','total7d','total30d','totalAllTime']]
        client.close()
        return refined_df
    except Exception as e:
        print(e)