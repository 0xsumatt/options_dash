import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scripts.llama import get_llama_vol_data,get_llama_prem_vol_data
from scripts.aevo import fetch_latest_volume,fetch_latest_prem_volume
import pandas as pd

st.warning("Information purposes only")
st.markdown("Welcome")
st.markdown("""
        On this site you can find
        - Volume stats for muliple on chain Options protocols
        - Fee stats for on aforementioned protocols alongside insurance fund balances (coming soon)
        - Call/Put ratios (coming soon)

        Data is collected through a mix of Defi Llama and my own database
        """)



def agg_data():
    st.header("Volume Charts")
    st.write("Data curtesy of Defi Llama")
    prem_vol_df = get_llama_prem_vol_data()
    not_vol_df = get_llama_vol_data()
    latest_volume = fetch_latest_volume()
    #latest_prem = fetch_latest_prem_volume()
    df_db = latest_volume.rename(columns={'daily_volume':'total24h'})
    #prem_db = latest_prem.rename(columns={'daily_volume_premium':'total24h'})
    vol_combined_df = pd.concat([df_db, not_vol_df], ignore_index=True)
    #prem_combined_df = prem_vol_df.append(prem_db,ignore_index = True)
   

    

    
    tf_options = st.radio("Select a Timeframe",["24H","7D","30D"],index =0,horizontal=True)
    graph_options = st.radio("Chart Type",["Bar","Pie"],index=0)
    col1,col2 = st.columns(2)
    if tf_options.lower() == '24h':
        fig_prem = px.bar(prem_vol_df, x=prem_vol_df['name'], y=prem_vol_df['total24h'], labels={'x':'Name', 'y':'Volume'}, title=f"Premium Volume over {tf_options} ")
        col1.plotly_chart(fig_prem,use_container_width=True)
        match graph_options.lower():
            case "bar":
                fig_vol = px.bar(vol_combined_df, x=vol_combined_df['name'], y=vol_combined_df['total24h'], labels={'x':'Name', 'y':'Notional Volume'}, title=f"Notional Volume over {tf_options}")
                col2.plotly_chart(fig_vol,use_container_width=True)
        
            case "pie":
                fig_vol_pie = go.Figure(data=go.Pie(labels=vol_combined_df['name'], values=vol_combined_df['total24h']))
                fig_vol_pie.update_layout(title='Notional Volume')
                col2.plotly_chart(fig_vol_pie,use_container_width=True)


        

    if tf_options.lower() == '7d':
        fig_prem = px.bar(prem_vol_df, x=prem_vol_df['name'], y=prem_vol_df['total7d'], labels={'x':'Name', 'y':'Volume'}, title=f"Premium Volume over {tf_options} ")
        col1.plotly_chart(fig_prem,use_container_width=True)

        match graph_options.lower():
            case "bar":
                fig_vol = px.bar(not_vol_df, x=not_vol_df['name'], y=not_vol_df['total7d'], labels={'x':'Name', 'y':'Notional Volume'}, title=f"Notional Volume over {tf_options}")
                col2.plotly_chart(fig_vol,use_container_width=True)
        
            case "pie":
                fig_vol_pie = go.Figure(data=go.Pie(labels=not_vol_df['name'], values=not_vol_df['total24h']))
                fig_vol_pie.update_layout(title='Notional Volume')
                col2.plotly_chart(fig_vol_pie,use_container_width=True)

    
    if tf_options.lower() == '30d':
        fig_prem = px.bar(prem_vol_df, x=prem_vol_df['name'], y=prem_vol_df['total30d'], labels={'x':'Name', 'y':'Volume'}, title=f"Premium Volume over {tf_options}")
        col1.plotly_chart(fig_prem,use_container_width=True)

        match graph_options.lower():
            case "bar":
                fig_vol = px.bar(not_vol_df, x=not_vol_df['name'], y=not_vol_df['total30d'], labels={'x':'Name', 'y':'Notional Volume'}, title=f"Notional Volume over {tf_options}")
                col2.plotly_chart(fig_vol,use_container_width=True)
        
            case "pie":
                fig_vol_pie = go.Figure(data=go.Pie(labels=not_vol_df['name'], values=not_vol_df['total30d']))
                fig_vol_pie.update_layout(title='Notional Volume')
                col2.plotly_chart(fig_vol_pie,use_container_width=True)
        
    
    



    
        

if __name__ == '__main__':
    agg_data()

    