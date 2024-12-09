import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Spatial Viz", page_icon="🌍")

st.markdown("# Spatial Visualization 🌍")
st.sidebar.header("Mapping Viz")
st.write(
    """This spatial visualize represents the relationship in countries column mapping with longtitude and latitude """
)

# Load the data with caching
@st.cache_data
def load_data():
    try:
        line_data_temp = pd.read_csv('./dataset/line_data_list.csv')
        expanded_df_temp = pd.read_csv('./dataset/countries.csv')
        return line_data_temp,expanded_df_temp
    except URLError as e:
        st.error(f"Failed to load data: {e}")


# Load the data
line_data,expanded_df =  load_data()

# ----------------- PyDeck Map Setup -----------------
# Create a PyDeck scatter plot layer for the countries (dots on the map)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    expanded_df,
    get_position='[longitude, latitude]',
    get_radius=50000,  # Adjust as needed
    get_fill_color=[0, 0, 255, 160],  # Blue with some transparency
    pickable=True,
)

# Create a PyDeck arc layer to show connection between countries
Outbound_Flow = pdk.Layer(
    "ArcLayer",
    data=line_data,
    get_source_position=["start_lon", "start_lat"],
    get_target_position=["end_lon", "end_lat"],
    get_source_color=[200, 30, 0, 160],
    get_target_color=[200, 30, 0, 160],
    auto_highlight=True,
    width_scale=0.0001,
    get_width="outbound",
    width_min_pixels=3,
    width_max_pixels=30,
),

# Set up the view for PyDeck
view_state = pdk.ViewState(
    latitude=8.199983,  # Center the map
    longitude=20.998022,
    zoom=0.5,
    pitch=30
)

# Create the PyDeck deck with both the line and scatter layers
deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[scatter_layer, Outbound_Flow],
    initial_view_state=view_state,
    tooltip={"text": "{Country}"}
)

# ----------------- Setup for map2 -----------------
# Create a PyDeck scatter plot layer for the countries (dots on the map)
scatter_layer2 = pdk.Layer(
    "ScatterplotLayer",
    expanded_df,
    get_position='[longitude, latitude]',
    get_radius=50000,  # Adjust as needed
    get_fill_color=[0, 0, 255, 160],  # Blue with some transparency
    pickable=True,
)

# Create a HeatpMap layer
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    expanded_df,
    get_position=['longitude','latitude'],
    opacity=0.8,
    pickable=True,
    radius_pixels=50,
)

# Set up the view for PyDeck
view_state2 = pdk.ViewState(
    latitude=8.199983,  # Center the map
    longitude=20.998022,
    zoom=0.5,
    pitch=0
)

deck2 = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[scatter_layer2,heatmap_layer],
    initial_view_state=view_state2,
    tooltip={"text": "{Country}"}
)


# ----------------- Render PyDeck Map -----------------
st.write(
    """### Spatial Visualization of Collaboration Between Countries"""
)
# Render the PyDeck map in Streamlit
# chart1
st.pydeck_chart(deck)

# chart2
st.write(
    """### Heatmap of Country that publish the research"""
)
st.pydeck_chart(deck2)
