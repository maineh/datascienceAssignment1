import os
import pandas as pd
from dateutil import parser

def delete_columns(df, columns_to_delete):
    # Check if the specified columns exist in the DataFrame before attempting deletion
    existing_columns = set(df.columns)
    columns_to_delete = [col for col in columns_to_delete if col in existing_columns]
    
    if columns_to_delete:
        df.drop(columns=columns_to_delete, inplace=True)
        print("Specified columns deleted successfully.")
    else:
        print("No specified columns found for deletion.")
    
    return df

available_currencies = set()
currency_conversion_to_euro = {}

def map_currency_conversion_rates(df):
    global currency_conversion_to_euro, available_currencies
    required_columns = [
        'Buyer Currency', 
        'Currency Conversion Rate', 
        'Merchant Currency'
    ]
    

    # Check if all required columns are in the DataFrame
    if all(column in df.columns for column in required_columns) and 'EUR' in df['Merchant Currency'].unique():
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Assuming the Merchant Currency is Euro, we directly take the conversion rate
            if row['Merchant Currency'] == 'EUR':
                currency = row['Buyer Currency']
                conversion_rate = row['Currency Conversion Rate']
                # Update the dictionary with the currency and its conversion rate to Euro
                currency_conversion_to_euro[currency] = conversion_rate
                available_currencies.add(currency)
        
        print("Currency conversion mapping processed.")
        print(currency_conversion_to_euro) 
    else:
        # Skip the file if required columns are not present or if merchant currency is not Euro
        print("Required columns for currency conversion mapping are not present or merchant currency is not Euro. Skipping file.")
    
    print("Available Currencies", available_currencies)
    return currency_conversion_to_euro, available_currencies


def standardize_column_names(df, column_mapping):
    standardized_columns = {}
    for col in df.columns:
        standardized_name = column_mapping.get(col, col)  # Get the standardized name if it exists
        standardized_columns[col] = standardized_name
    df.rename(columns=standardized_columns, inplace=True)
    return df

def filter_function(file_path, product_id, column_mapping):
    dtype = {'Amount (Merchant Currency)': float}
    df = pd.read_csv(file_path, dtype=dtype)
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
    'Product id': 'Product ID',
    'Product ID': 'Product ID',
    'Sku Id': 'SKU ID',
    'SKU ID': 'SKU ID',
    'Buyer Country': 'Country of Buyer',
    'Country of Buyer': 'Country of Buyer',
    'Buyer Postal Code': 'Buyer Postal Code',  
    'Postal Code of Buyer': 'Buyer Postal Code',  

}

for filename in os.listdir(directory):
    if filename.endswith('.csv') and filename.startswith('sales_'): 
        file_path = os.path.join(directory, filename)
        
        filtered_df = filter_function(file_path, product_id, column_mapping)  # Pass column_mapping as an argument
        processed_df = process_data(filtered_df)
        currency_conversion_to_euro, available_currencies = map_currency_conversion_rates(processed_df)  # Assuming merged_df is your merged DataFrame
        print("Total Available Currencies", available_currencies)
        
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

def convert_charged_amount(df, currency_conversion_to_euro):
    result_df = pd.DataFrame()  # Initialize an empty DataFrame for the results

    for index, row in df.iterrows():
        currency = row['Currency of Sale']
        if pd.isnull(currency):  # Check for NaN currency
            print(f"Row with index {index} has NaN currency. Skipping conversion.")
            result_df = pd.concat([result_df, pd.DataFrame([row])], ignore_index=True)
            continue  # Skip the rest of the loop for this row

        # Check if the currency is in the available currencies set
        if currency in available_currencies:
            # Convert the 'Charged Amount'
            try:
                converted_amount = (float(row['Charged Amount'].replace(',', '')) * currency_conversion_to_euro[currency]
                                    ) if isinstance(row['Charged Amount'], str) else row['Charged Amount'] * currency_conversion_to_euro[currency]
                converted_amount = round(converted_amount, ndigits=2)
                row['Charged Amount'] = converted_amount
                result_df = pd.concat([result_df, pd.DataFrame([row])], ignore_index=True)
            except KeyError:
                # Handle the case where the conversion rate is missing
                print(f"Missing conversion rate for currency: {currency}")
        else:
            print(f"Row with index {index} and currency {currency} is being removed.")

    print("Conversion and filtering completed.")
    return result_df
    

def merge_columns(df):
    # Check if both columns exist in the DataFrame before attempting merge
    if 'Charged Amount' in df.columns and 'Amount (Merchant Currency)' in df.columns:
        df['Amount (Merchant Currency)'] = df.apply(lambda row: row['Charged Amount'] if pd.notna(row['Charged Amount']) else row['Amount (Merchant Currency)'], axis=1)
        print("Columns merged successfully.")
    if 'Financial Status' in df.columns and 'Transaction Type' in df.columns:
        df['Transaction Type'] = df.apply(lambda row: 'Charge' if row['Financial Status'] == 'Charged' else row['Transaction Type'], axis=1)
        print("Columns merged successfully.")
    else:
        print("Required columns for merging are not present.")

    return df


# After all operations are done, but before the merged file is saved, call the convert_charged_amount function

print("At this point, i'm converting the currencies", available_currencies)

pre_conversion_file_path = os.path.join(".\\processed_data", 'sales_pre_conversion_merged.csv')
merged_df.to_csv(pre_conversion_file_path, index=False)
print(f'Pre-conversion merged file saved to: {pre_conversion_file_path}')

print("Currency conversion rates:", currency_conversion_to_euro)
if currency_conversion_to_euro:
    merged_df = convert_charged_amount(merged_df, currency_conversion_to_euro)

merged_df = merge_columns(merged_df)
    
columns_to_delete = ['Timestamp', 'Tax Status', 'Refund Type', 'Financial Status','Product Type','Hardware', 'Buyer State', 'Buyer Currency', 'Amount (Buyer Currency)','Currency Conversion Rate', 'Merchant Currency', 'Base Plan ID', 'Offer ID','Device Model',	'Currency of Sale'	,'Item Price',	'Taxes Collected','Charged Amount',	'City of Buyer',	'State of Buyer'  ]  # Specify columns to delete here  # noqa: E999
merged_df = delete_columns(merged_df, columns_to_delete)  # Update merged_df with the result of delete_columns

def filter_transaction_type(df):
    if 'Transaction Type' in df.columns:
        df = df[df['Transaction Type'] == 'Charge']
        print("Filtered on Transaction Type: Charge.")
    else:
        print("Transaction Type column not found. Skipping filtering.")
    return df

# # Before saving the merged file, apply the filter function
merged_df = filter_transaction_type(merged_df)

# Save the merged DataFrame to a new CSV file
merged_file_path = os.path.join(".\\merged_data", 'sales_merged.csv')
merged_df.to_csv(merged_file_path, index=False)

print(f'Merged file saved to: {merged_file_path}')