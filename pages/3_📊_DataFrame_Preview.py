import streamlit as st
import pandas as pd


st.set_page_config(page_title="DataFrame Preview", page_icon="📊")

st.markdown("# DataFrame Preview")
st.sidebar.header("DataFrame Preview")
st.write(
    """### DataFrame Preview: Visualizing Data in Our Web Application
In this web application, we provide an interactive and user-friendly way to explore the underlying data that drives our visualizations. Using **Streamlit**, we allow users to preview and filter the dataset directly within the app. This makes it easier to understand how the data contributes to the visualizations and insights you see.
"""
)

# Display the dataframe in Streamlit
data = pd.read_csv('data/updated_with_year.csv')
selected_year = st.selectbox('Select Year', options=data['year'].unique())
st.dataframe(data[data['year'] == selected_year].reset_index(drop=True))


