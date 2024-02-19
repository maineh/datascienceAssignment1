import pandas as pd
import os

# Directory where your CSV files are stored, update this path as necessary
directory = './assignment1 data'

# List of file names based on the naming pattern
file_names = [f'stats_ratings_{year}{month:02d}_country.csv' for year in [2021] for month in range(6,13)]

# Initialize an empty list to store DataFrames
dataframes = []

# Loop through the file names, read each file into a DataFrame, and append it to the list
for file_name in file_names:
    file_path = os.path.join(directory, file_name)
    try:
        # Try reading with UTF-16 encoding if UTF-8 fails
        df = pd.read_csv(file_path, encoding='utf-16')
        dataframes.append(df)
    except UnicodeDecodeError:
        # Fall back to UTF-8 or another encoding as needed
        df = pd.read_csv(file_path, encoding='utf-8')
        dataframes.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
country_stats_merged = pd.concat(dataframes, ignore_index=True)

# Convert the 'Date' column to datetime format
country_stats_merged['Date'] = pd.to_datetime(country_stats_merged['Date'])

# Sort the DataFrame by the 'Date' column
country_stats_merged = country_stats_merged.sort_values(by='Date')

# Display the first few rows to verify the DataFrame
print(country_stats_merged.head())

