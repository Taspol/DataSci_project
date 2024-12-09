import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)


@st.cache_data
def from_data_file(filename):
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename
    )
    return pd.read_json(url)


try:
    ALL_LAYERS = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[exits]",
            radius_scale=0.05,
        ),
        "Bart Stop Names": pdk.Layer(
            "TextLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }
    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 37.76,
                    "longitude": -122.4,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )

# Create a PyDeck line layer to plot the lines between countries
line_data = pd.read_csv('./dataset/line_data_list.csv')
expanded_df = pd.read_csv('./dataset/countries.csv')
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