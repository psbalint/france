import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="French Villages",
    page_icon="🗺️",
    layout="wide",
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv("villages.csv")


# --------------------------------------------------
# Remove overseas locations
# --------------------------------------------------

overseas = [
    "Guyane",
    "Martinique",
    "Guadeloupe",
    "La Réunion",
    "Mayotte",
    "Saint-Pierre-et-Miquelon",
    "Polynésie française",
    "Nouvelle-Calédonie",
    "Wallis-et-Futuna",
    "Saint-Martin",
    "Saint-Barthélemy",
]

df = df[~df["Département"].isin(overseas)]


# --------------------------------------------------
# Remove rows without coordinates
# --------------------------------------------------

df = df.dropna(
    subset=["latitude", "longitude"]
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("Le Village préféré des Français")

st.write(
    f"{len(df)} locations from metropolitan France"
)


# --------------------------------------------------
# Create France map
# --------------------------------------------------

m = folium.Map(
    location=[46.6, 2.2],
    zoom_start=6,
    tiles="OpenStreetMap",
)


# --------------------------------------------------
# Add markers
# --------------------------------------------------

for _, row in df.iterrows():

    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"],
        ],
        radius=7,
        color="white",
        weight=2,
        fill=True,
        fill_color="#1a73e8",
        fill_opacity=1,
        tooltip=row["Village"],
        popup=folium.Popup(
            f"""
            <b>{row["Village"]}</b><br>
            Département: {row["Département"]}<br>
            Région: {row["Région"]}<br>
            Placement: {row["Placement"]}<br>
            Year: {row["Year"]}
            """,
            max_width=300,
        ),
    ).add_to(m)


# --------------------------------------------------
# Display map
# --------------------------------------------------

st_folium(
    m,
    width=1200,
    height=900,
)
