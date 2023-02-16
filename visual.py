import streamlit as st
import pandas as pd
import altair as alt
import mysql.connector

st.set_page_config(layout="wide",
page_title="PhonePe Pulse DataViz",
page_icon="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/phonepe-logo-icon.png")
st.image('https://cdn.worldvectorlogo.com/logos/phonepe-1.svg', width=100)
st.title("Data Explorer")
# st.balloons()
col1, col2, col3, col4 = st.columns((2,1,1,1))

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="rk",
    password="rk123",
    database="guvi_phonePe"
)

# Define a function to retrieve data from the database

# map_trans = pd.read_sql_query("SELECT *  FROM map_trans", mydb)
m_locations = pd.read_sql_query("SELECT *  FROM m_locations", mydb)



def get_options(filter_name):
    query = f"SELECT DISTINCT {filter_name} FROM map_trans"
    df = pd.read_sql_query(query, mydb)
    options = list(df[filter_name])
    return options


# Add dropdowns for the year and name filters
with st.sidebar:
    year_options = get_options("year")
    year = st.selectbox("Select Year", year_options)

    qtr_options = get_options("qtr")
    qtr = st.selectbox("Select Qtr", qtr_options)


    # Get the data based on the selected filters

    # Add a select box for the measure
    measure_options = ['Total Amount', '# of Transaction','Average Amount Per Transaction']
    measure = st.selectbox("Select Measure", measure_options)

# st.button("label", key=None, help=None, on_click=None, args=None, kwargs=None, *, type="secondary", disabled=False, use_container_width=False)

# tab1, tab2, tab3 = st.tabs(qtr_options)
# Get the data based on the selected filters and measure
if measure == 'Total Amount':
    query = "SELECT country,state,district, SUM(amount) as total_measure FROM map_trans WHERE year=%s AND qtr=%s and state<>'' GROUP BY country,state,district"
    measure_label = 'Total Amount'
elif measure == '# of Transaction':
    query = "SELECT country,state,district, SUM(count) as total_measure FROM map_trans WHERE year=%s AND qtr=%s and state<>'' GROUP BY country,state,district"
    measure_label = '# of Transaction'
elif measure == 'Average Amount Per Transaction':
    query = "SELECT country,state,district, SUM(amount)/SUM(count) as total_measure FROM map_trans WHERE year=%s AND qtr=%s and state<>'' GROUP BY country,state,district"
    measure_label = '# of Transaction'
else:
    query = "SELECT country,state,district, sum(amount) as total_measure FROM map_trans WHERE year=%s AND qtr=%s and state<>'' GROUP BY country,state,district"
    measure_label = 'Transaction Count'

# Get the data based on the selected filters and measure
params = (year, qtr)
df = pd.read_sql_query(query, mydb, params=params)
map_user_location=pd.merge(df, m_locations, on=['country', 'state', 'district'])

# Create the bar chart using Altair
chart = alt.Chart(df).mark_bar().encode(
    x='district:N',
    y='total_measure:Q'
)

chart2 = alt.Chart(df).mark_line().encode(
    x='district:N',
    y='total_measure:Q'
)


# /////////////////////////////////////////////////////////////////////////////////////

import plotly.express as px

# Remove rows where lat_long is None
map_viz = map_user_location[map_user_location["lat_long"].notnull()]

# Split the lat_long column into separate latitude and longitude columns
# map_viz["latitude"] = map_viz["lat_long"].apply(lambda x: x[0])
# map_viz["longitude"] = map_viz["lat_long"].apply(lambda x: x[1])

map_viz["latitude"] = map_viz["lat_long"].str.extract(r"\((.*),")
map_viz["longitude"] = map_viz["lat_long"].str.extract(r", (.*)\)")

# Convert the columns to numeric
map_viz["latitude"] = pd.to_numeric(map_viz["latitude"], errors='coerce')
map_viz["longitude"] = pd.to_numeric(map_viz["longitude"], errors='coerce')

# Filter out rows where lat and long are NaN
map_viz = map_viz.dropna(subset=["latitude", "longitude"])

# Create a scatter mapbox plot using Plotly Express
fig = px.scatter_mapbox(map_viz, lat="latitude", lon="longitude", hover_name="district",
                        color="total_measure", size="total_measure", size_max=30, zoom=4, height=700)


# # Update the map style and show the figure
fig.update_layout(mapbox_style="carto-positron")
fig.update_traces(textposition='top center')
# fig.show()

st.plotly_chart(fig, theme=None, use_container_width=True)
st.write(map_viz)




# # Create the bar chart using Altair
# chart = alt.Chart(df).mark_bar().encode(
#     x='state:N',
#     y='total_amount:Q',
#     tooltip=['state:N', 'total_amount:Q', 'total_count:Q']
# )

# # Set the chart title and axis labels
# chart = chart.properties(
#     title=f"Total Amount by State for {year} ({name})",
#     width=600,
#     height=400
# ).configure_axis(
#     labelFontSize=12,
#     titleFontSize=14
# )

# # Display the chart in the Streamlit app
# st.altair_chart(chart, use_container_width=True)
# st.write(df)
# # Set the chart title and axis labels
# chart = chart.properties(
#     title=f"{measure_label} by State for {year} ({qtr})",
#     width=600,
#     height=400
# ).configure_axis(
#     labelFontSize=12,
#     titleFontSize=14
# )

# # Display the chart in the Streamlit app
# col1, col2, col3, col4 = st.columns((4,1,1,1))
# with col1:
#     st.altair_chart(chart, use_container_width=True)
# st.altair_chart(chart2, use_container_width=True)
