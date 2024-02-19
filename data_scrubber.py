import os
import pandas as pd
from dateutil import parser

def standardize_column_names(df, column_mapping):
    standardized_columns = {}
    for col in df.columns:
        standardized_name = column_mapping.get(col, col)  # Get the standardized name if it exists
        standardized_columns[col] = standardized_name
    df.rename(columns=standardized_columns, inplace=True)
    return df

def filter_function(file_path, product_id, column_mapping):
    df = pd.read_csv(file_path)
    df = standardize_column_names(df, column_mapping)  # Standardize column names here
    filtered_df = df[df['Product ID'].str.contains(product_id)]  # Use the standardized column name
    return filtered_df

def process_data(df):
    df['Date'] = df['Date'].apply(parser.parse)  # Make sure 'Date' is the standardized column name
    # Additional preprocessing steps can be added here
    return df

directory = '.\\assignment1 data'
product_id = 'com.vansteinengroentjes.apps.ddfive'
column_mapping = {
    'Description': 'Transaction ID',
    'Order Number': 'Transaction ID',
    'Transaction Date': 'Date',
    'Order Charged Date': 'Date',
    'Transaction Time': 'Timestamp',
    'Order Charged Timestamp': 'Timestamp',
    'Tax Type': 'Tax Status',
    'Financial Status': 'Tax Status',
    'Product id': 'Product ID',
    'Product ID': 'Product ID',
    'Sku Id': 'SKU ID',
    'SKU ID': 'SKU ID',
    'Buyer Country': 'Country of Buyer',
    'Country of Buyer': 'Country of Buyer',
    # Add other mappings as necessary
}

for filename in os.listdir(directory):
    if filename.endswith('.csv') and filename.startswith('sales_'): 
        file_path = os.path.join(directory, filename)
        
        filtered_df = filter_function(file_path, product_id, column_mapping)  # Pass column_mapping as an argument
        processed_df = process_data(filtered_df)
        
        save_directory = '.\\processed_data'
        processed_file_name = os.path.basename(file_path).replace('.csv', '_processed.csv')
        processed_file_path = os.path.join(save_directory, processed_file_name)
        processed_df.to_csv(processed_file_path, index=False)
        
        print(f'Processed file saved to: {processed_file_path}')
        
processed_files = os.listdir(save_directory)
all_dfs = []  # List to store all DataFrames

for file in processed_files:
    if file.endswith('_processed.csv'):  # Ensure to only include processed files
        file_path = os.path.join(save_directory, file)
        df = pd.read_csv(file_path)
        all_dfs.append(df)

# Concatenate all DataFrames in the list
merged_df = pd.concat(all_dfs, ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_file_path = os.path.join(".\\merged_data", 'sales_merged.csv')
merged_df.to_csv(merged_file_path, index=False)

print(f'Merged file saved to: {merged_file_path}')