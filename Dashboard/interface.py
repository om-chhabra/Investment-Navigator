import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df =  pd.read_csv('./startup.csv')
df.head()
# Streamlit Dashboard

st.title("Startup Dashboard")
st.sidebar.header("Filters")

# Filter by Sector
sectors = st.sidebar.multiselect("Choose Sectors", df['Sector'].unique())
if not sectors:
    sectors = df['Sector'].unique()
filtered_data = df[df['Sector'].isin(sectors)]

# Display data in a table
st.write(filtered_data)

# Bar plot of Total Funding Raised by Startup
fig = px.bar(filtered_data, x='Startup Name', y='Total Funding Raised', title="Total Funding Raised by Startup")
st.plotly_chart(fig)

# Bar plot of Total Revenue by Startup
fig2 = px.bar(filtered_data, x='Startup Name', y='Total Revenue', title="Total Revenue by Startup")
st.plotly_chart(fig2)

# Map visualization for Location (assuming a dummy lat-long for cities, in a real-world scenario, you'd need accurate coordinates)
city_coordinates = {
    'Bangalore': [12.9716, 77.5946],
    'Mumbai': [19.0760, 72.8777],
    'Delhi': [28.6139, 77.2090],
    'Chennai': [13.0827, 80.2707],
    'Bengaluru': [12.9716, 77.5946]
}

filtered_data['lat'] = filtered_data['Location'].map(lambda x: city_coordinates.get(x, [0, 0])[0])
filtered_data['lon'] = filtered_data['Location'].map(lambda x: city_coordinates.get(x, [0, 0])[1])

fig3 = px.scatter_geo(filtered_data,
                      lat='lat',
                      lon='lon',
                      scope='asia',
                      hover_name='Startup Name',
                      title='Startup Locations in India',
                      template='plotly',
                      opacity=0.6,
                      size='Total Funding Raised',
                      projection="mercator",
                      )
fig3.update_geos(
    projection_type="mercator",  # You can choose a projection type
    lataxis_range=[6, 40],  # Latitude range for India
    lonaxis_range=[68, 98]   # Longitude range for India
)

fig3.update_layout(width=800, height=800)
st.plotly_chart(fig3)

# Note: You'd need more data preprocessing for optimal results, and more visualizations can be added as needed.