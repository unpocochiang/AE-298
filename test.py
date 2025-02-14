import re
import requests
import pandas as pd
from io import StringIO

# URL of the CSV file
airfoil_name = 'marske7-il'
re = 50000
url = f'http://airfoiltools.com/polar/csv?polar=xf-{airfoil_name}-{re}'

# Send GET request
response = requests.get(url)

if response.status_code == 200:
    # Convert response text into a readable format
    csv_data = StringIO(response.text)
    
    # Read CSV, skipping metadata
    df = pd.read_csv(csv_data, skiprows=10)

    # Save DataFrame to CSV file
    filename = f'{airfoil_name}_{re}.csv'
    df.to_csv(filename, index=False)
else:
    print("Failed to download CSV. Status Code:", response.status_code)
