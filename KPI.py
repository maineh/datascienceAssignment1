import os
import pandas as pd
from dateutil import parser
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry

# Directory where your CSV files are stored, update this path as necessary
directory = './merged_data'

sales_file = ['sales_merged.csv']
# List of CSV files containing country statistics and sales data
country_stats_file = ['country_stats_merged.csv']
ratings_file = ['ratings_merged.csv']
crashes_file = ['crashes_merged.csv']


for file in sales_file:
    if file.endswith('merged.csv'):  # Ensure to only include processed files
        file_path = os.path.join(directory, file)
        sales_df = pd.read_csv(file_path)
print(sales_df.head())

for file in crashes_file:
    if file.endswith('merged.csv'):  # Ensure to only include processed files
        file_path = os.path.join(directory, file)
        crashes_df = pd.read_csv(file_path)
print(crashes_df.head())

# Loop through each country statistics file
for file in country_stats_file:
    # Check if the file name ends with 'merged.csv'
    if file.endswith('merged.csv'):
        # Construct the file path
        file_path = os.path.join(directory, file)
        # Read the CSV file into a DataFrame
        country_stats_df = pd.read_csv(file_path)

# Loop through each country statistics file
for file in ratings_file:
    # Check if the file name ends with 'merged.csv'
    if file.endswith('merged.csv'):
        # Construct the file path
        file_path = os.path.join(directory, file)
        # Read the CSV file into a DataFrame
        ratings_df = pd.read_csv(file_path)

#The following lines describe a KPI based on Sales volume
# Convert 'Date' to datetime object
sales_df['Date'] = pd.to_datetime(sales_df['Date'])

# Extract date attributes into new columns
sales_df['Year'] = sales_df['Date'].dt.year
sales_df['Month'] = sales_df['Date'].dt.month
sales_df['Day'] = sales_df['Date'].dt.day

#The data is grouped by month 
#This line calculates the average amount of money per transaction per month
average_amount_by_month = sales_df.groupby('Month')['Amount (Merchant Currency)'].mean()
print(average_amount_by_month)
#This line calculates the monthly revenue and growth
monthly_revenue = sales_df.groupby('Month')['Amount (Merchant Currency)'].sum()
print(monthly_revenue)


monthly_transaction_count = sales_df.groupby('Month')['Transaction ID'].count()
print(monthly_transaction_count)
# Calculate Monthly Growth Percentage
monthly_revenue_growth = monthly_revenue.pct_change() * 100
monthly_transaction_count_growth = monthly_transaction_count.pct_change() * 100

# Create a Plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Monthly Revenue Growth
ax1.plot(monthly_revenue_growth, color='blue', marker='o', label='Revenue Growth (%)')
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue Growth (%)', color='blue')
ax1.tick_params('y', colors='blue')
ax1.legend(loc='upper left')

# Create a secondary y-axis for Transaction Count
ax2 = ax1.twinx()
ax2.plot(monthly_transaction_count_growth, color='green', marker='s', label='Transaction Count Growth (%)')
ax2.set_ylabel('Transaction Count Growth (%)', color='green')
ax2.tick_params('y', colors='green')
ax2.legend(loc='upper right')

plt.title('Monthly Growth Percentage: Revenue and Transaction Count')
plt.show()


#KPI that shows Product Rate per month
monthly_grouped_data = sales_df.groupby('Month')
# Step 2: Group by 'Product Title' within each month and count transactions
monthly_transaction_count_per_product = monthly_grouped_data.apply(lambda x: x.groupby('Product Title')['Transaction ID'].count().reset_index(name='Transaction_Count'))

# Display the result
print(monthly_transaction_count_per_product)

fig, ax = plt.subplots(figsize=(10, 5))
color_mapping = {'Product Title 1': 'pink', 'Product Title 2': 'blue'} 
color_mapping1=[color_mapping.get(title, 'gray') for title in monthly_transaction_count_per_product['Product Title']]
sns.barplot(x='Month', y='Transaction_Count', hue='Product Title', data=monthly_transaction_count_per_product, palette = ['blue', 'pink'], ax=ax)

# Display the result
plt.title('Monthly Transactions per Product Type')
plt.xlabel('Month')
plt.ylabel('Transactions')
plt.show()


#KPI that shows Product Rate per month
monthly_grouped_data = sales_df.groupby('Month')
# Step 2: Group by 'Product Title' within each month and count transactions
monthly_transaction_count_per_sku = monthly_grouped_data.apply(lambda x: x.groupby('SKU ID')['Transaction ID'].count().reset_index(name='Transaction_Count'))

# Display the result
print(monthly_transaction_count_per_sku)

fig, ax = plt.subplots(figsize=(10, 5))
color_mapping = {'SKU ID 0': 'pink', 'SKU ID 1': 'blue'} 
color_mapping1=[color_mapping.get(title, 'gray') for title in monthly_transaction_count_per_sku['SKU ID']]
sns.barplot(x='Month', y='Transaction_Count', hue='SKU ID', data=monthly_transaction_count_per_sku, palette = ['blue', 'pink'], ax=ax)

# Display the result
plt.title('Monthly Transactions per SKU ID')
plt.xlabel('Month')
plt.ylabel('Transactions')
plt.show()

# Create a new column 'weekday' containing the weekday for each date (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
sales_df['Weekday'] = sales_df['Date'].dt.weekday
sales_df['Month'] = sales_df['Date'].dt.month

# Display the DataFrame with the new 'weekday' column
print(sales_df[['Date', 'Weekday']])


# Create a pivot table for the heatmap
heatmap_data = sales_df.pivot_table(index = 'Month', columns='Weekday', values='Transaction ID', aggfunc='count')

# Create a Plot
fig, ax = plt.subplots(figsize=(12, 8))

# Use seaborn to create a heatmap
sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='g', linewidths=.5, cbar_kws={'label': 'Transaction Count'})

# Display the result
plt.title('Heatmap of Transaction Count Based on Day of the Week and Time of the Day')
plt.xlabel('Day of the Week')
plt.ylabel('Month of the Week')
plt.show()

# Create a dictionary to map two-letter country codes to ISO Alpha-3 codes
country_code_mapping = {country.alpha_2: country.alpha_3 for country in pycountry.countries}
# Map the codes in your DataFrame using the dictionary
country_stats_df['Country'] = country_stats_df['Country'].map(country_code_mapping)
sales_df['Country'] = sales_df['Country of Buyer'].map(country_code_mapping)

# Convert the 'Date' column to datetime format
country_stats_df['Date'] = pd.to_datetime(country_stats_df['Date'])

# Sales volume per country
sales_by_country = sales_df.groupby('Country')['Transaction ID'].count().reset_index()

sales_map_fig = px.choropleth(sales_by_country,
                              locations="Country",
                              color="Transaction ID",
                              hover_name="Country",
                              projection="natural earth",
                              title="Total Sales Volume by Country",
                              color_continuous_scale="turbo")  # Adjust color scale as desired

# Show the figure
sales_map_fig.show()

# Create a Plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Daily Average Rating
ax1.plot(ratings_df['Date'], ratings_df['Daily Average Rating'].astype(float), marker='o', markersize=5, label='Daily Avg Rating', color='blue', linewidth=1)
ax1.set_xlabel('Date')
ax1.set_ylabel('Ratings', color='blue')
ax1.tick_params('y', colors='blue')
ax1.legend(loc='upper left')

# Create a secondary y-axis for Transaction Count
ax2 = ax1.twinx()
ax2.plot(crashes_df['Date'], crashes_df['Daily Crashes'].astype(float), marker='x', markersize=5, label='Daily Crashes', color='red', linewidth=1)
ax2.set_ylabel('Amount of Daily Crashes', color='red')
ax2.tick_params('y', colors='red')
ax2.legend(loc='upper right')


plt.title('Crashes and Daily Rating')
plt.show()