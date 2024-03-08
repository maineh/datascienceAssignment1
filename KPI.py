import os
import pandas as pd
from dateutil import parser
import matplotlib.pyplot as plt
import seaborn as sns

# Directory where your CSV files are stored, update this path as necessary
directory = './merged_data'

file_name = ['sales_merged.csv']


for file in file_name:
    if file.endswith('merged.csv'):  # Ensure to only include processed files
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)

#The following lines describe a KPI based on Sales volume
# Convert 'Date' to datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Extract date attributes into new columns
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

#The data is grouped by month 
#This line calculates the average amount of money per transaction per month
average_amount_by_month = df.groupby('Month')['Amount (Merchant Currency)'].mean()
print(average_amount_by_month)
#This line calculates the monthly revenue and growth
monthly_revenue = df.groupby('Month')['Amount (Merchant Currency)'].sum()
print(monthly_revenue)

monthly_transaction_count = df.groupby('Month')['Transaction ID'].count()
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
#plt.show()

# Filter rows where 'Amount' is higher than 20 to see what goes wrong in month 11
filtered_data = df[df['Amount (Merchant Currency)'] > 20]
print(filtered_data)



#KPI that shows Product Rate per month
monthly_grouped_data = df.groupby('Month')
# Step 2: Group by 'Product Title' within each month and count transactions
monthly_transaction_count_per_product = monthly_grouped_data.apply(lambda x: x.groupby('Product Title')['Transaction ID'].count().reset_index(name='Transaction_Count'))

# Display the result
print(monthly_transaction_count_per_product)

fig, ax = plt.subplots(figsize=(12, 6))


sns.barplot(x='Month', y='Transaction_Count', hue='Product Title', data=monthly_transaction_count_per_product, ax=ax)

# Display the result
plt.title('Monthly Transactions per Product Type')
plt.xlabel('Month')
plt.ylabel('Transactions')
plt.show()