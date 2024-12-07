import streamlit as st
import time
import numpy as np
import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from collections import Counter
from analyze_function.data_insights import analyze_funding_agencies
from analyze_function.data_insights import article_per_year
from analyze_function.data_insights import analyze_top_cited_journals
from analyze_function.data_insights import analyze_open_access_trends
from analyze_function.data_insights import analyze_connection_node


# Load the uploaded CSV file to inspect its structure and contents
file_path = 'dataset/updated_with_year.csv'
data = pd.read_csv(file_path)
data.info()

# Set page configuration
st.set_page_config(page_title="Data Insight", page_icon="📈",layout='wide')

# Set title and description
st.sidebar.header("Data Insight")
st.write(
    """# Welcome to Data Insights Visualize 🌟

This is the **Data Insights Visualize** platform for our project, where we bring data to life through intuitive and interactive visualizations. Designed to showcase the core findings and trends, this tool serves as the visual representation of the data driving our project."""
)

## ---------------visualize data part---------------
col1, col2 = st.columns(2)
## top cited journals
with col1:
    fig1 = analyze_top_cited_journals(data, top_n=10)
    st.plotly_chart(fig1)

## open access trends
with col2:
    fig2 = analyze_open_access_trends(data)
    st.plotly_chart(fig2)

col1, col2 = st.columns(2)

## funding agencies sorted by keyword
with col1:
    option = st.selectbox(
        "Select Available Keywords:",
        ("Chulalongkorn", "NSTDA", "Thailand Research Fund" , "Mahidol University", "Kasetsart University","Thailand","Chiang Mai University","Khon Kaen University","Prince of Songkla University","Suranaree University of Technology"),
        index=None,
        placeholder="Select keywords...",
    )
    if not option:
        option = "Chulalongkorn"
    fig3 = analyze_funding_agencies(data, keyword=option, column_name='Funding Agencies', top_n=10)
    st.plotly_chart(fig3)

## article per year
with col2:
    fig4 = article_per_year(data)
    st.plotly_chart(fig4)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

## connection node
fig5 = analyze_connection_node(data)
st.plotly_chart(fig5)


last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)
for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()
st.button("Re-run")