import streamlit as st
import time
import numpy as np
import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from collections import Counter

## ---------------data analysis part---------------
# Function to analyze top-cited journals
def analyze_top_cited_journals(data, top_n=10):
    """
    Analyze and visualize the top-cited journals, handling long text labels.

    Parameters:
        data (DataFrame): The dataset containing journal and citation data.
        top_n (int): The number of top-cited journals to visualize.

    Returns:
        None: Displays a bar chart of top-cited journals.
    """
    # Identify top-cited journals
    top_cited = data.groupby('prism:publicationName')['citedby-count'].sum().sort_values(ascending=False).head(top_n)
    
    # Truncate or format long journal names
    top_cited.index = top_cited.index.map(lambda x: x[:20] + "..." if len(x) > 20 else x)

    # Plot the top-cited journals
    fig = px.bar(
        top_cited,
        x=top_cited.index,
        y=top_cited.values,
        title=f"Top {top_n} Journals by Total Citations",
        color_discrete_sequence=['skyblue']
    )
    fig.update_layout(
        xaxis_title="Journal Names",
        yaxis_title="Total Citations",
        xaxis_tickangle=-45,
        height=500,
        width=800
    )
    return fig


def analyze_open_access_trends(data):
    """
    Analyze and visualize the open-access trends.

    Parameters:
        data (DataFrame): The dataset containing open-access flag data.

    Returns:
        None: Displays a pie chart of open-access vs closed access trends.
    """
    # Analyze open-access trends
    open_access_trends = data['openaccessFlag'].value_counts()

    # Plot open-access trends
    fig = px.pie(
        names=open_access_trends.index,
        values=open_access_trends.values,
        title="Open Access vs Closed Access",
        color=open_access_trends.index,
        color_discrete_sequence=['lightgreen', 'lightcoral'],
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label', pull=[0, 0.1])
    return fig


def analyze_funding_agency_counts(data, top_n=10):
    """
    Display the top funding agencies by count.

    Parameters:
        data (DataFrame): The dataset containing funding agency data.
        top_n (int): The number of top funding agencies to display.

    Returns:
        None: Prints the top funding agencies by count.
    """
    # Explore funding patterns
    funding_counts = data['Funding Agencies'].value_counts().head(top_n)

    print(f"Top {top_n} Funding Agencies by Count:")
    print(funding_counts)

# Function to filter rows containing a specific keyword in the Funding Agencies column
def filter_by_funding_agency(data, keyword, column_name='Funding Agencies'):
    return data[data[column_name].str.contains(keyword, case=False, na=False)]

# Function to extract co-occurring funding agencies (excluding a specific keyword)
def extract_co_occurring_agencies(filtered_data, keyword, column_name='Funding Agencies'):
    co_occurring_agencies = []
    for _, row in filtered_data.iterrows():
        agencies = row[column_name].split(',')
        # Exclude the keyword from the agency list
        agencies = [agency.strip() for agency in agencies if keyword.lower() not in agency.lower()]
        co_occurring_agencies.extend(agencies)
    return co_occurring_agencies

# Function to count the frequency of co-occurring agencies
def count_co_occurrences(co_occurring_agencies):
    return Counter(co_occurring_agencies)

# Function to prepare a DataFrame for visualization
def prepare_top_agencies_df(co_occurrence_count, top_n):
    top_co_occurring_agencies = co_occurrence_count.most_common(top_n)
    return pd.DataFrame(top_co_occurring_agencies, columns=['Agency', 'Count'])

# Function to create a bar plot using Plotly
def plot_top_agencies(top_agencies_df, top_n, keyword):
    top_agencies_df.Agency = top_agencies_df.Agency.map(lambda x: x[:20] + "..." if len(x) > 20 else x)
    fig = px.bar(
        top_agencies_df, 
        x='Agency', 
        y='Count',
        title=f"Top {top_n} Funding Agencies Most Related to {keyword}",
        labels={'Agency': 'Funding Agency', 'Count': 'Co-occurrence Count'},
        color='Count', 
        color_continuous_scale='Viridis',

    )

    fig.update_layout(
        xaxis_tickangle=-45,
    )
    return fig

# Renamed main function for workflow execution
def analyze_funding_agencies(data, keyword='Chulalongkorn', column_name='Funding Agencies', top_n=10):
    # Step 1: Filter data by keyword
    filtered_data = filter_by_funding_agency(data, keyword, column_name)
    
    # Step 2: Extract co-occurring agencies
    co_occurring_agencies = extract_co_occurring_agencies(filtered_data, keyword, column_name)
    
    # Step 3: Count co-occurrence frequencies
    co_occurrence_count = count_co_occurrences(co_occurring_agencies)
    
    # Step 4: Prepare a DataFrame for the top N agencies
    top_agencies_df = prepare_top_agencies_df(co_occurrence_count, top_n)
    
    # Step 5: Plot the results
    return plot_top_agencies(top_agencies_df, top_n, keyword)

def article_per_year(data):
    articles_per_year = data.groupby('year').size()

    # Create the line plot
    fig = px.line(articles_per_year, title='Number of Articles Published per Year', labels={'year': 'Year', '0': 'Number of Articles'})

    # Update the layout to improve the chart aesthetics
    fig.update_layout(
        title='Number of Articles Published per Year',  # Title of the plot
        title_x=0.33,  # Center the title
        xaxis_title='Year',  # X-axis title
        yaxis_title='Number of Articles',  # Y-axis title
        xaxis=dict(
            tickmode='linear',  # Make sure that the x-axis shows years consistently
            tickformat='%Y',  # Format x-axis labels as years
            showgrid=True,  # Show gridlines on the x-axis
            gridcolor='lightgray',
        ),
        yaxis=dict(
            showgrid=True,  # Show gridlines on the y-axis
            gridcolor='lightgray',  # Color of the gridlines
            zeroline=True,  # Show a line at y=0
            zerolinecolor='black',  # Color of the y=0 line
        ),
        plot_bgcolor='whitesmoke',  # Background color of the plot
        paper_bgcolor='white',  # Background color of the paper area
        margin=dict(l=120, r=50, t=180, b=50),  # Adjust the margins
        height=500,  # Set the height of the plot
    )
    # Add markers to the line for each year to make the data points more visible
    fig.update_traces(
        mode='lines+markers',  # Show both the line and markers
        marker=dict(color='red', size=8, line=dict(width=2, color='black')),  # Marker properties
        line=dict(color='blue', width=3)  # Line properties
    )
    fig.add_vline(x=2020, line=dict(color='purple', width=2, dash='dash'), annotation_text="Pandemic Year", annotation_position="top right")
    return fig 
## ---------------data analysis part---------------