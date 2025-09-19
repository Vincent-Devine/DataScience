import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ----------------------------
# 1️⃣ Example Numpy computation
# ----------------------------
v1 = np.array([1, 2, 3])
v2 = np.array([1, 1, 1])
v3 = v1 + v2
print("Example numpy addition:", v3)

# ----------------------------
# 2️⃣ Load Dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("drinks.csv", index_col=0)  # assuming first column is index
    return df

drinks = load_data()

# ----------------------------
# 3️⃣ Sidebar Filters
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

# ----------------------------
# 4️⃣ Bar Chart Visualization
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
# 5️⃣ Summary Statistics
# ----------------------------
st.header("Summary Statistics")
st.write(filtered_data[[selected_drink]].describe())

# ----------------------------
# 6️⃣ Top 10 Countries
# ----------------------------
st.header(f"Top 10 Countries by {selected_drink.replace('_', ' ').title()}")
top10 = filtered_data.sort_values(by=selected_drink, ascending=False).head(10)
st.dataframe(top10[['country', selected_drink]])

# ----------------------------
# 7️⃣ World Map Visualization
# ----------------------------
st.header(f"World Map of {selected_drink.replace('_', ' ').title()}")

fig_map = px.choropleth(
    filtered_data,
    scope="europe",
    color=selected_drink,
    color_continuous_scale=px.colors.sequential.Plasma,
)
st.plotly_chart(fig_map, use_container_width=True)
