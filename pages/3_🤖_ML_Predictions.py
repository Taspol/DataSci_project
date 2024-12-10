import streamlit as st
import pandas as pd
from analyze_function.ml_processing import analyze_category
from analyze_function.ml_processing import analyze_webscrape
from app.data_collection.db import MongoDBHandler

st.set_page_config(page_title="ML_Processing", page_icon="🤖",layout='wide')

st.markdown("# ML_Processing 🤖")
st.sidebar.header("ML_Processing")
st.write(
    """### Visualizing Data in Our Web Application
"""
)

data = pd.read_csv('dataset/k-mean.csv')
fig1 = analyze_category(data)
st.plotly_chart(fig1)

st.write(
    """### Visualizing category of data from OpenRex"
"""
)
db_Handler = MongoDBHandler()
data5 =  pd.read_csv('dataset/title_field_count.csv')
fig2 = analyze_webscrape(data5)
st.plotly_chart(fig2)








