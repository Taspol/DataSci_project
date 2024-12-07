import streamlit as st
import pandas as pd
from analyze_function.ml_processing import analyze_category

st.set_page_config(page_title="ML_Processing", page_icon="🤖",layout='wide')

st.markdown("# ML_Processing 🤖")
st.sidebar.header("ML_Processing")
st.write(
    """### ML_Processing: Visualizing Data in Our Web Application
"""
)

data = pd.read_csv('dataset/k-mean.csv')
fig1 = analyze_category(data)
st.plotly_chart(fig1)





