"""Data Extraction and Loading"""

import os
import json
import pandas as pd
import requests
import zipfile
import urllib3
from zipfile import ZipFile
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set Kaggle API credentials (ensure kaggle.json is in ~/.kaggle or %USERPROFILE%\.kaggle\)
kaggle_json_path = os.path.join(os.getenv('USERPROFILE'), '.kaggle', 'kaggle.json')

# Load Kaggle API credentials from the kaggle.json file
with open(kaggle_json_path, 'r') as file:
    kaggle_credentials = json.load(file)
    kaggle_username = kaggle_credentials['username']
    kaggle_key = kaggle_credentials['key']

# Kaggle API endpoint and headers
dataset_url = 'https://www.kaggle.com/api/v1/datasets/download/dinachanthan/cleaned-retail-shop-dataset'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': f'Bearer {kaggle_key}'
}

# Create the data directory if it doesn't exist
data_dir = './data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Download the dataset with SSL verification disabled
response = requests.get(dataset_url, headers=headers, stream=True, verify=False)

# Use a temporary in-memory buffer to handle the zip file
zip_buffer = BytesIO()

total_size = int(response.headers.get('content-length', 0))
chunk_size = total_size // 4

if response.status_code == 200:
    for chunk in response.iter_content(chunk_size=chunk_size):
        zip_buffer.write(chunk)

    # Verify if the file is a valid zip file
    zip_buffer.seek(0)
    if zipfile.is_zipfile(zip_buffer):
        # Extract the dataset using ThreadPoolExecutor for parallel processing
        with ZipFile(zip_buffer, 'r') as zip_ref:
            def extract_file(file):
                zip_ref.extract(file, data_dir)

            with ThreadPoolExecutor() as executor:
                executor.map(extract_file, zip_ref.namelist())

        # Find the CSV file in the extracted files
        extracted_files = os.listdir(data_dir)
        csv_files = [file for file in extracted_files if file.endswith('.csv')]

        if not csv_files:
            raise FileNotFoundError("No CSV file found in the extracted dataset.")
        
        data_path = os.path.join(data_dir, csv_files[0])

        # Load a sample of the dataset to infer data types
        total_rows = sum(1 for _ in open(data_path)) - 1  # Subtract 1 for the header
        ten_percent_rows = int(total_rows * 0.10)
        sample_df = pd.read_csv(data_path, nrows=ten_percent_rows)
        dtype_spec = sample_df.dtypes.apply(lambda x: x.name).to_dict()

        # Optimize data types for pandas
        for column, dtype in dtype_spec.items():
            if dtype.startswith('int'):
                dtype_spec[column] = 'Int64'  # Use pandas nullable integer type
            elif dtype.startswith('float'):
                dtype_spec[column] = 'float64'
            elif dtype == 'object':
                dtype_spec[column] = 'category'

        # Use 'pyarrow' for faster CSV reading if available, fallback to default 'c' engine
        try:
            df = pd.read_csv(data_path, engine='pyarrow', dtype=dtype_spec)
        except ImportError:
            df = pd.read_csv(data_path, engine='c', dtype=dtype_spec)

        print('\nKaggle data loaded successfully\n')
    else:
        print("The downloaded file is not a valid zip file")
else:
    print(f"Failed to download the dataset. Status code: {response.status_code}")