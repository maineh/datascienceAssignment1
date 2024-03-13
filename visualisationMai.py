# Import necessary libraries
import os
import pandas as pd
from dateutil import parser
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry


# Directory where your CSV files are stored, update this path as necessary
directory = './merged_data'

# List of CSV files containing country statistics and sales data
country_stats_file = ['country_stats_merged.csv']
sales_file = ['sales_merged.csv']

# Loop through each country statistics file
for file in country_stats_file:
    # Check if the file name ends with 'merged.csv'
    if file.endswith('merged.csv'):
        # Construct the file path
        file_path = os.path.join(directory, file)
        # Read the CSV file into a DataFrame
        country_stats_df = pd.read_csv(file_path)

for file in sales_file:
    # Check if the file name ends with 'merged.csv'
    if file.endswith('merged.csv'):
        # Construct the file path
        file_path = os.path.join(directory, file)
        # Read the CSV file into a DataFrame
        sales_df = pd.read_csv(file_path)

# Create a dictionary to map two-letter country codes to ISO Alpha-3 codes
country_code_mapping = {country.alpha_2: country.alpha_3 for country in pycountry.countries}
# Map the codes in your DataFrame using the dictionary
country_stats_df['Country'] = country_stats_df['Country'].map(country_code_mapping)
sales_df['Country'] = sales_df['Country of Buyer'].map(country_code_mapping)

# Convert the 'Date' column to datetime format
country_stats_df['Date'] = pd.to_datetime(country_stats_df['Date'])



# Average rating per country per day

avg_rating_per_country_per_day_fig = px.scatter_geo(country_stats_df,
                     locations="Country",  # Assumes 'Country' contains ISO country codes
                     size="Total Average Rating",  # Bubble size based on total average rating
                     color="Total Average Rating",  # Color based on total average rating
                     animation_frame=country_stats_df['Date'].dt.strftime('%Y-%m-%d'),
                     hover_name="Country",  # Tooltip shows country name
                     projection="natural earth",
                     title="Total Average Rating by Country",
                     color_continuous_scale="viridis",  # Vibrant color scale
                     range_color=[1,5])  # Range covering the full scope of ratings
avg_rating_per_country_per_day_fig.show()

# Sales volume per country
sales_by_country = sales_df.groupby('Country')['Amount (Merchant Currency)'].sum().reset_index()

sales_map_fig = px.choropleth(sales_by_country,
                              locations="Country",
                              color="Amount (Merchant Currency)",
                              hover_name="Country",
                              projection="natural earth",
                              title="Total Sales Volume by Country",
                              color_continuous_scale="viridis")  # Adjust color scale as desired

# Show the figure
sales_map_fig.show()




