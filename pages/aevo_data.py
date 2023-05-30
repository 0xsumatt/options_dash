import pandas as pd
from scripts.aevo import *
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.markdown("""
On this page you can find:
- Current Put/Call ratio as well as historic (Coming soon currently collecting data)
- Volumes in both USD and Contract terms
- Perp Data (also coming soon)
""")
            
st.markdown("Please note data is currently being collected so timestamps on both the put call ratio and number of put & call contracts will update overtime")
            
put_call = fetch_put_call()

fig1 = px.line(put_call, x = put_call['timestamp'], y = put_call['put_call_ratio'], labels ={'x':"Data", 'y':"Put Call Ratio"}, title = "Historic Put Call Ratios")
st.plotly_chart(fig1)
graph_choice = st.radio("Chart Type",["Bar","Pie"],index=0)
c1,c2 = st.columns(2)
oi_data = fetch_OI()
oi_hist = fetch_hist_OI()

if graph_choice.lower()=='bar':
    oi_fig = px.bar(oi_data, x='Type', y='Open Interest', title="Open Interest by Option Type", color='Type', color_discrete_sequence=oi_data['Color'])
    c1.plotly_chart(oi_fig,use_container_width=True)
    # Create a stacked bar chart
    fig = go.Figure(data=[
        go.Bar(name='Puts', x=oi_hist['timestamp'], y=oi_hist['puts'], marker_color='red'),
        go.Bar(name='Calls', x=oi_hist['timestamp'] ,y=oi_hist['calls'], marker_color='green')
    ])
    
    # Change the bar mode
    fig.update_layout(barmode='stack', title_text='Historical Puts & Calls Daily (Histogram)' )

    c2.plotly_chart(fig,use_container_width=True)


else:
    oi_fig = fig = go.Figure(data=[go.Pie(labels=oi_data['Type'], values=oi_data['Open Interest'], marker_colors=['green', 'red'])])

    c1.plotly_chart(oi_fig,use_container_width=True)

