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

def get_options(filter_name):
    query = f"SELECT DISTINCT {filter_name} FROM agg_trans"
    df = pd.read_sql_query(query, mydb)
    options = list(df[filter_name])
    return options


# Add dropdowns for the year and name filters
with st.sidebar:
    year_options = get_options("year")
    year = st.selectbox("Select Year", year_options)

    name_options = get_options("name")
    name = st.selectbox("Select Name", name_options)


    # Get the data based on the selected filters

    # Add a select box for the measure
    measure_options = ['Total Amount', '# of Transaction','Average Amount Per Transaction']
    measure = st.selectbox("Select Measure", measure_options)

# st.button("label", key=None, help=None, on_click=None, args=None, kwargs=None, *, type="secondary", disabled=False, use_container_width=False)

# tab1, tab2, tab3 = st.tabs(name_options)
# Get the data based on the selected filters and measure
if measure == 'Total Amount':
    query = "SELECT state, SUM(amount) as total_measure FROM agg_trans WHERE year=%s AND name=%s and state<>'' GROUP BY state"
    measure_label = 'Total Amount'
elif measure == '# of Transaction':
    query = "SELECT state, SUM(count) as total_measure FROM agg_trans WHERE year=%s AND name=%s and state<>'' GROUP BY state"
    measure_label = '# of Transaction'
elif measure == 'Average Amount Per Transaction':
    query = "SELECT state, SUM(amount)/SUM(count) as total_measure FROM agg_trans WHERE year=%s AND name=%s and state<>'' GROUP BY state"
    measure_label = '# of Transaction'
else:
    query = "SELECT state, sum(amount) as total_measure FROM agg_trans WHERE year=%s AND name=%s and state<>'' GROUP BY state"
    measure_label = 'Transaction Count'

# Get the data based on the selected filters and measure
params = (year, name)
df = pd.read_sql_query(query, mydb, params=params)

# Create the bar chart using Altair
chart = alt.Chart(df).mark_bar().encode(
    x='state:N',
    y='total_measure:Q'
)

chart2 = alt.Chart(df).mark_line().encode(
    x='state:N',
    y='total_measure:Q'
)

# Set the chart title and axis labels
chart = chart.properties(
    title=f"{measure_label} by State for {year} ({name})",
    width=600,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

# Display the chart in the Streamlit app
col1, col2, col3, col4 = st.columns((4,1,1,1))
with col1:
    st.altair_chart(chart, use_container_width=True)
st.altair_chart(chart2, use_container_width=True)

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
