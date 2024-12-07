import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to our project! 👋")

st.sidebar.success("Select visualization from the sidebar to get started.")

import streamlit as st

# Streamlit Introduction Page
st.markdown("""
# Data Science Project: Pipeline for Data Engineering, Machine Learning, and Visualization

Welcome to the **Data Science Pipeline** project! This application demonstrates the seamless integration of:

- **Data Engineering (DE)**: Efficiently preprocess and clean data for analysis.
- **Machine Learning (ML)**: Build, train, and evaluate predictive models.
- **Visualization (Viz)**: Present insights through interactive charts and dashboards.

## Objectives
The primary goals of this project are:
1. **Streamline workflows** by automating data preprocessing, feature engineering, and model training.
2. **Promote interpretability** through meaningful visualizations of both raw and processed data.
3. **Demonstrate scalability** in handling datasets of varying sizes and complexities.

## Key Features
- **Data Engineering**: 
  - Handle missing data, outliers, and transformations.
  - Data integration and feature extraction pipelines.

- **Machine Learning**: 
  - Explore models such as linear regression, classification, clustering, and more.
  - Hyperparameter tuning and performance evaluation.

- **Visualization**:
  - Interactive plots and dashboards for data exploration.
  - Model performance metrics and trend analysis.

## How to Use the App
    adding later


## About
This project is designed for:
- Data scientists and analysts looking to explore end-to-end workflows.
- Researchers and students seeking hands-on experience in implementing pipelines.
- Organizations interested in building scalable and automated systems.

---

Explore the features by navigating through the sidebar!

""")
