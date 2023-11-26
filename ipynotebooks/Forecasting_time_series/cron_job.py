import requests
import pandas as pd
import pprint
import csv
from datetime import datetime

# NISE
NISE = "nise gwal"
NISE_STATION = "NISE Gwal Pahari, Gurugram, India"

# Sector 51
SECTOR_51 = "Sector-51, Gurugram"
SECTOR_51_STATION = "Sector-51, Gurugram, India"

# Teri gram
TERI_GRAM = "Teri Gram, Gurugram"
TERI_GRAM_STATION = "Teri Gram, Gurugram"

# Vikas Sadan
VIKAS_SADAN = "Vikas Sadan Gurgaon"
VIKAS_SADAN_STATION = "Vikas Sadan Gurgaon"

# Incase if api fails, write to file with previous day

def setData(station, station_location):
    url = "https://api.waqi.info/search/?token=7c0e1c5a796cf1a14edf4bf1462a99e9b37d8bdf&keyword="+station
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()
        result = []
        if res["data"][0]['station']['name'] == station_location:
            result.append(res["data"][0]['aqi'])
            result.append(res["data"][0]['station']['name'])
            result.append(pd.to_datetime(res["data"][0]['time']['stime']))
        print(station, result) 

        # Write to the file only when (station, time) is not already existing in the file.
        
        new_timestamp = (res["data"][0]['time']['stime'])
        csv_file_path = 'ipynotebooks/Forecasting_time_series/output.csv'

        # Check if the new timestamp is already present
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Assuming the timestamp is in the 3rd column
            existing_timestamps = [row[2] for row in csv_reader]
        
        if new_timestamp not in existing_timestamps:
            with open(csv_file_path, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows([result])
            print(f'The data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
        else:
            print(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')

    else:
        print(f"Error: {response.status_code} - {response.text}")

setData(NISE, NISE_STATION)
