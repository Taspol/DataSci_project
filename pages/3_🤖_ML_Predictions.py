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

# File uploader for custom input
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the user-provided dataset
    data5 = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded dataset:")
    st.write(data5.head())  # Display a preview of the dataset
    
    # Call your function to visualize the data
    fig2 = analyze_webscrape(data5)
    st.plotly_chart(fig2)
else:
    st.write("Please upload a CSV file to visualize.")








