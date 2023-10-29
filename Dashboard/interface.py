import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
from geopy.geocoders import Nominatim

# url_to_redirect = "http://localhost:8501/predict"

# if st.sidebar.button('Advance Analytics'):
#     # HTML anchor tag to open the URL in a new tab
#     st.markdown(f'<a href="{url_to_redirect}" target="_blank">Click here to visit the website</a>', unsafe_allow_html=True)

df =  pd.read_csv('./startup.csv')
df['Founding Year'] = df['Founding Year'].astype(str)
# Streamlit Dashboard
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

st.title("Startup Dashboard")
st.sidebar.header("Filters")

# Filter by Sector
sectors = st.sidebar.multiselect("Choose Sectors", df['Sector'].unique())
if not sectors:
    sectors = df['Sector'].unique()
filtered_data = df[df['Sector'].isin(sectors)]

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

revenue_columns = ['2018 Rev', '2019 Rev', '2020 Rev', '2021 Rev', '2022 Rev', '2023 Rev']
st.title("Revenue Chart for COVID Impact")
# Ensure revenue columns are numeric
for col in revenue_columns:
    filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')

# Calculate average revenue by year for the selected sectors
average_revenues = filtered_data[revenue_columns].mean(axis=0)

# Line chart for yearly average revenue
st.line_chart(average_revenues, use_container_width=True)

total_funding = df['Total Funding Raised'].sum()
sector_funding = df.groupby('Sector')['Total Funding Raised'].sum().reset_index()
sector_funding['Percent'] = (sector_funding['Total Funding Raised'] / total_funding) * 100
sector_funding['Sector'] = sector_funding.apply(lambda x: x['Sector'] if x['Percent'] > 2.5 else 'Others', axis=1)
grouped_funding = sector_funding.groupby('Sector').sum().reset_index()

fig_pie_funding = px.pie(grouped_funding, values='Total Funding Raised', names='Sector', 
                         title='Total Funding by Sector', 
                         color='Sector',
                         color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_pie_funding)


total_companies = len(df)
sector_counts = df['Sector'].value_counts().reset_index()
sector_counts.columns = ['Sector', 'Count']
sector_counts['Percent'] = (sector_counts['Count'] / total_companies) * 100
sector_counts['Sector'] = sector_counts.apply(lambda x: x['Sector'] if x['Percent'] > 2.5 else 'Others', axis=1)
grouped_counts = sector_counts.groupby('Sector').sum().reset_index()

# Pie chart for total count of companies per sector
fig_pie_count = px.pie(grouped_counts, values='Count', names='Sector', 
                       title='Number of Companies by Sector', 
                       color='Sector',
                       color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_pie_count)

df['Age'] = 2023 - df['Founding Year'].astype(int)
fig_scatter = px.scatter(df, x='Age', y='CAGR', hover_data=['Startup Name'], 
                         title='CAGR vs Age of Companies', 
                         color_discrete_sequence=px.colors.qualitative.Set3)

st.plotly_chart(fig_scatter)

sector_funding = df.groupby('Sector')['Total Funding Raised'].sum().reset_index()

# Creating the donut chart
fig = px.pie(sector_funding, names='Sector', values='Total Funding Raised', hole=0.3,
             title="Total Funding Raised by Sector")
fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1])  # Adjust this for a "pulled apart" look

# Displaying the chart in Streamlit
st.plotly_chart(fig)

funding_rounds = ['Series A', 'Series B', 'Series C', 'Series D']
purposes = ['Series A Purpose', 'Series B Purpose', 'Series C Purpose', 'Series D Purpose']
vis_data = pd.DataFrame(columns=['Funding Round', 'Purpose', 'Count'])

for round_, purpose in zip(funding_rounds, purposes):
    purpose_counts = df[purpose].value_counts().reset_index()
    purpose_counts.columns = ['Purpose', 'Count']
    purpose_counts['Funding Round'] = round_
    vis_data = pd.concat([vis_data, purpose_counts])

# Create the stacked bar chart
fig_stacked_bar = px.bar(vis_data, x='Funding Round', y='Count', color='Purpose', 
                         title='Startup Funding Purposes by Round', 
                         color_discrete_sequence=px.colors.qualitative.Set3)

# Display the chart in Streamlit
st.plotly_chart(fig_stacked_bar)


# Display in streamlit
st.plotly_chart(fig)

# Function to determine the current funding round
def get_current_funding_round(row):
    for round_ in ['Series D', 'Series C', 'Series B', 'Series A']:
        if row[round_] > 0:
            return round_
    return None

# Apply the function to get the current funding round for each startup
df['Current Funding Round'] = df.apply(get_current_funding_round, axis=1)

# Filter out startups without any funding round info
data_filtered = df.dropna(subset=['Current Funding Round'])

# Create the scatter plot
fig = px.scatter(data_filtered, x='Current Funding Round', y='CAGR', hover_data=['Startup Name'],
                 title='Current Funding Round vs CAGR',
                 category_orders={'Current Funding Round': ['Series A', 'Series B', 'Series C', 'Series D']},
                 color_discrete_sequence=px.colors.qualitative.Set3)

# Display the chart in Streamlit
st.plotly_chart(fig)

df_fintech = df[df['Sector'] == 'Fintech']

# Computing Valuations for each year
for year in range(2019, 2024):
    column_name = f'{year} Valuation'
    revenue_column = f'{year} Rev'
    df_fintech[column_name] = df_fintech[revenue_column] * 6

# Calculating average valuation for each year
average_valuations = {}
for year in range(2019, 2024):
    column_name = f'{year} Valuation'
    average_valuations[str(year)] = df_fintech[column_name].mean()

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
years = list(average_valuations.keys())
avg_values = list(average_valuations.values())
ax.plot(years, avg_values, marker='o', label='Average Valuation')

ax.set_title('Average Valuation-based Analysis of Fintech Sector (2019-2023)')
ax.set_xlabel('Year')
ax.set_ylabel('Average Valuation (Million $)')
ax.legend()
ax.grid(True)

st.pyplot(fig)

df_counts = df['Location'].value_counts().reset_index()
df_counts.columns = ['Location', 'Startup Count']

# Fetching latitudes and longitudes for each location
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get latitude and longitude from city name
def get_lat_lon(city):
    location = geolocator.geocode(city + ", India")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

df['count'] = 1
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


# filtered_data['lat'] = filtered_data['Location'].map(lambda x: city_coordinates.get(x, [0, 0])[0])
# filtered_data['lon'] = filtered_data['Location'].map(lambda x: city_coordinates.get(x, [0, 0])[1])

# fig3 = px.scatter_geo(filtered_data,
#                       lat='lat',
#                       lon='lon',
#                       scope='asia',
#                       hover_name='Startup Name',
#                       title='Startup Locations in India',
#                       template='plotly',
#                       opacity=0.6,
#                       size='Total Funding Raised',
#                       projection="mercator",
#                       )
# fig3.update_geos(
#     projection_type="mercator",  # You can choose a projection type
#     lataxis_range=[6, 40],  # Latitude range for India
#     lonaxis_range=[68, 98]   # Longitude range for India
# )

# fig3.update_layout(width=800, height=800)
# st.plotly_chart(fig3)

# Note: You'd need more data preprocessing for optimal results, and more visualizations can be added as needed.