import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from geopy.geocoders import Nominatim

# Load Data
df = pd.read_csv('./startup.csv')
df['Founding Year'] = df['Founding Year'].astype(str)

news_df = pd.DataFrame({
    'Sector': ['EV', 'EV','EV','EV','EV','AI','AI','AI','AI','AI'],
    'Header': ['Tesla, EV Investors Face a Reckoning', 'Joe Biden Green Energy Flop: Automakers Realize Americans Are Not Buying Electric Vehicles', "Ford, GM, and even Tesla are warning about the EV market","Ford, GM, and even Tesla are warning about the EV market","Decoding The Chaos In The Market For Electric Cars","AI Revolution Shakes Silicon Valley","AI Ethics Take Center Stage","Neural Networks: The Backbone of Modern AI","AI in Healthcare: A Blessing or a Curse?","AI-Powered Drones: The Future of Surveillance"],
    'Description': [
        'The electric-vehicle boom that spawned multibillion dollar startups overnight and pushed Tesla Inc.’s value into the stratosphere is starting to flounder just a few years after it began. • None Israel Latest: Iranian Minister Warns US Over Support of Israel ',
        'American automakers are quickly learning that Americans are not buying electric vehicles (EVs) at the rates they expected.',
        'Ford announced on Thursday that it delaying a $12 billion investment in electric vehicle (EV) manufacturing facilities, including halting the construction of a second battery plant in Kentucky, per CNBC. Ford said in a media briefing on Thursday that growth i',
        'The electric-vehicle boom that spawned multibillion dollar startups overnight and pushed Tesla Inc.’s value into the stratosphere is starting to flounder just a few years after it began. • None US Military Attacks Two Syrian Facilities It Says Are Linked to...',
        'Headwinds for electric cars are increasing as higher interest rates make them less affordable for mainstream buyers.',
        "The artificial intelligence surge that initiated numerous tech unicorns and boosted AI startups' valuations is now facing significant challenges amidst global data concerns.",
        "Emerging concerns over AI ethics and fairness have led to major tech giants revisiting their AI research strategies, prompting a new wave of transparent research methodologies.",
    "Deep learning techniques, primarily neural networks, are pushing the boundaries of what's possible, transforming industries and creating unprecedented efficiencies.",
    "The rapid adoption of AI in diagnostics and patient care has raised eyebrows, leading to debates over its reliability and the potential risks associated with it.",
    "Next-generation drones, backed by powerful AI algorithms, are revolutionizing surveillance, delivery, and reconnaissance operations globally."]
})

# Streamlit Dashboard
st.title("Startup Dashboard")
st.sidebar.header("Filters")

# Filter by Sector
sectors = st.sidebar.multiselect("Choose Sectors", df['Sector'].unique())
filtered_data = df[df['Sector'].isin(sectors)] if sectors else df

# News Feed Filter
st.sidebar.header("News Feed" )
selected_sector = st.sidebar.selectbox('Select a sector to view news', ['AI', 'EV'])
filtered_news = news_df[news_df['Sector'] == selected_sector]
for _, row in filtered_news.iterrows():
    st.sidebar.header(row['Header'])
    st.sidebar.write(row['Description'])
st.sidebar.markdown("[Go to News Feed](https://newsapi.org/v2/top-headlines?country=us&category=business)")

# Display data in a table
st.write(filtered_data)

# Bar plot of Total Funding Raised by Startup
fig = px.bar(filtered_data, x='Startup Name', y='Total Funding Raised', title="Total Funding Raised by Startup")
st.plotly_chart(fig)

# Bar plot of Total Revenue by Startup
fig2 = px.bar(filtered_data, x='Startup Name', y='Total Revenue', title="Total Revenue by Startup")
st.plotly_chart(fig2)

# Line chart for yearly average revenue
revenue_columns = ['2018 Rev', '2019 Rev', '2020 Rev', '2021 Rev', '2022 Rev', '2023 Rev']
for col in revenue_columns:
    filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')
average_revenues = filtered_data[revenue_columns].mean(axis=0)
st.line_chart(average_revenues, use_container_width=True)

# Heat Map of Companies
geolocator = Nominatim(user_agent="geoapiExercises")
df['count'] = 1

# Function to get latitude and longitude from city name
def get_lat_lon(city):
    location = geolocator.geocode(city + ", India")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

df['latitude'], df['longitude'] = zip(*df['Location'].apply(get_lat_lon))
df = df.dropna(subset=['latitude', 'longitude'])
df_grouped = df.groupby(['Location', 'latitude', 'longitude']).sum().reset_index()

layer = pdk.Layer(
    "HeatmapLayer",
    df_grouped,
    opacity=0.5,
    get_position=["longitude", "latitude"],
    aggregator_name="SUM",
    get_weight="count",
    radius=200
)

view_state = pdk.ViewState(latitude=20.5937, longitude=78.9629, zoom=4)  # Over India
r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v9")
st.title("Heat Map of Companies")
st.pydeck_chart(r)