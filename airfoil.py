import requests
import os
import pandas as pd
from io import StringIO


def airfoil_shape(airfoil):
    url = f'https://m-selig.ae.illinois.edu/ads/coord/{airfoil}.dat'
    
    folder = "airfoils"
    os.makedirs(folder, exist_ok=True)

    # Define filename and URL
    filename = f'{airfoil}.dat'
    # Full path to save
    filepath = os.path.join(folder, filename)

    response = requests.get(url)

    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)

def airfoil_data(airfoil_name, re):
    re_list = [50000, 100000, 200000, 500000, 1000000]
    closest = min(re_list, key=lambda x: abs(x - re))
    url = f'http://airfoiltools.com/polar/csv?polar=xf-{airfoil_name}-{closest}'
    
    # Define folder to save the CSV
    filepath = os.path.join('airfoils', f'{airfoil_name}_{closest}.csv')

    # Send GET request
    response = requests.get(url)

    if response.status_code == 200:
        # Convert response text into a readable format
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, skiprows=10)
        df.to_csv(filepath, index=False)
    else:
        print("Failed to download CSV. Status Code:", response.status_code)
        print(f'link: {url}')
