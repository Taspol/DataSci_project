import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write(
    """This spatial visualize to see colaboration of each country in each paper."""
)
@st.cache_data
def load_data():
    try:
        line_data_temp = pd.read_csv('./dataset/line_data_list.csv')
        expanded_df_temp = pd.read_csv('./dataset/countries.csv')
        return line_data_temp,expanded_df_temp
    except URLError as e:
        st.error(f"Failed to load data: {e}")


# Create a PyDeck line layer to plot the lines between countries
line_data,expanded_df =  load_data()

line_layer = pdk.Layer(
    "PathLayer",
    line_data,
    get_path='[[start_lon, start_lat], [end_lon, end_lat]]',
    get_color=[255, 0, 0],  # Red lines
    width_scale=10,
    width_min_pixels=2
)

# Create a PyDeck scatter plot layer for the countries (dots on the map)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    expanded_df,
    get_position='[longitude, latitude]',
    get_radius=50000,  # Adjust as needed
    get_fill_color=[0, 0, 255, 160],  # Blue with some transparency
    pickable=True,
)
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
    latitude=20,  # Center the map
    longitude=100,
    zoom=1,
    pitch=30
)

# Create the PyDeck deck with both the line and scatter layers
deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[    scatter_layer, Outbound_Flow],
    initial_view_state=view_state,
    tooltip={"text": "{Country}"}
)

# Render the PyDeck map in Streamlit
st.pydeck_chart(deck)