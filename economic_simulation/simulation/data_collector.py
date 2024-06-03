import os
import pandas as pd
from fredapi import Fred

# Set your FRED API key here
fred = Fred(api_key='YOUR_API_KEY')

# Function to fetch data from FRED
def fetch_data(series_id, start_date, end_date):
    data = fred.get_series(series_id, start_date, end_date)
    return data

# Create necessary directories if they don't exist
output_dir = 'simulation/static/simulation/data'
os.makedirs(output_dir, exist_ok=True)

# Example: Fetching GDP data
gdp_data = fetch_data('GDP', '2000-01-01', '2020-01-01')
gdp_data.to_csv(os.path.join(output_dir, 'gdp_data.csv'))

# Add more data fetching as needed
# inflation_data = fetch_data('CPIAUCSL', '2000-01-01', '2020-01-01')
# unemployment_data = fetch_data('UNRATE', '2000-01-01', '2020-01-01')
