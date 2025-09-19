import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# ----------------------------
# Load Dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("drinks.csv", index_col=0)  # assuming first column is index
    return df

drinks = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

# Select type of drink
drink_types = ['beer_servings', 'wine_servings', 'spirit_servings', 'total_litres_of_pure_alcohol']
selected_drink = st.sidebar.selectbox("Select Drink Type", drink_types)

# Optional: filter by continent if column exists
if 'continent' in drinks.columns:
    continents = drinks['continent'].dropna().unique()
    selected_continent = st.sidebar.multiselect("Select Continent(s)", continents, default=continents)
    filtered_data = drinks[drinks['continent'].isin(selected_continent)]
else:
    filtered_data = drinks.copy()

# Slider
age = st.sidebar.slider("Average consumer age", 0, 100, 25)
income = st.sidebar.slider("Average consumer income", 0, 30000, (10000, 20000), 500)
temperature = st.sidebar.slider("Average temperature", -15, 45, 20)

# ----------------------------
# Bar Chart Visualization
# ----------------------------
st.title(f"Alcohol Consumption Analysis: {selected_drink}")

fig_bar = px.bar(
    filtered_data.sort_values(by=selected_drink, ascending=False),
    x='country',
    y=selected_drink,
    color='continent' if 'continent' in filtered_data.columns else None,
    title=f"{selected_drink.replace('_', ' ').title()} by Country",
    labels={selected_drink: selected_drink.replace('_', ' ').title(), 'country': 'Country'}
)
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------
# Summary Statistics
# ----------------------------
st.header("Summary Statistics")
st.write(filtered_data[[selected_drink]].describe())

# ----------------------------
# Top 10 Countries
# ----------------------------
st.header(f"Top 10 Countries by {selected_drink.replace('_', ' ').title()}")
top10 = filtered_data.sort_values(by=selected_drink, ascending=False).head(10)
st.dataframe(top10[['country', selected_drink]])

# ----------------------------
# World Map Visualization
# ----------------------------
st.header(f"World Map of {selected_drink.replace('_', ' ').title()}")

fig_map = px.choropleth(
    filtered_data,
    scope="europe",
    color=selected_drink,
    color_continuous_scale=px.colors.sequential.Plasma,
)
st.plotly_chart(fig_map, use_container_width=True)
