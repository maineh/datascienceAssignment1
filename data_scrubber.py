import os
import pandas as pd

def filter_function(file_path, product_id):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Filter the DataFrame to only include rows where the 'Product ID' column contains the desired text
    filtered_df = df[df['Product ID'].str.contains(product_id)]

    return filtered_df

def process_data(df):
    # Perform cleaning and preprocessing steps here
    # For example, convert 'Transaction Date' to datetime format
    # Make sure 'Transaction Date' is the correct column name in your CSV files
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%b %d, %Y')
    
    # You can add more preprocessing steps here as needed
    
    return df

# Define the directory containing the CSV files and the product ID to filter by
directory = 'C:\Users\jsdew\Documents\GitHub\datascienceAssignment1\assignment1 data'
product_id = 'com.vansteinengroentjes.apps.ddfive'

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        
        # Use the filter_function to filter the data
        filtered_df = filter_function(file_path, product_id)
        
        # Use the process_data function to perform additional data cleaning and preprocessing
        processed_df = process_data(filtered_df)
        
        # Save the processed DataFrame back to CSV
        processed_file_path = file_path.replace('.csv', '_processed.csv')
        processed_df.to_csv(processed_file_path, index=False)
        
        print(f'Processed file saved to: {processed_file_path}')