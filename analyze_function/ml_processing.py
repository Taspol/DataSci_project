import streamlit as st
import time
import numpy as np
import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from collections import Counter

def analyze_category(data):
    fig = px.scatter(data, x='PCA1', y='PCA2', color='auto_label', 
                 hover_data={ "dc:title":True},
                 title="Cluster Visualization with Auto-Labeling",
                 labels={'auto_label': 'Research Field'},
                 height=900
                 )

    return fig