import requests
import pandas as pd
import pprint
import csv
from datetime import datetime, timedelta
import logging
import os
import logging.handlers

# NISE
NISE = "nise gwal"
NISE_STATION = "NISE Gwal Pahari, Gurugram, India"
NISE_OUTPUT = "../../data/cron_job_data/nise_cron_output"

# Sector 51
SECTOR_51 = "Sector-51, Gurugram"
SECTOR_51_STATION = "Sector-51, Gurugram, India"
SECTOR_51_OUTPUT = "../../data/cron_job_data/sector_51_cron_output"

# Teri gram
TERI_GRAM = "Teri Gram"
TERI_GRAM_STATION = "Teri Gram, Gurugram"
TERI_GRAM_OUTPUT = "../../data/cron_job_data/teri_gram_cron_output"

# Vikas Sadan
VIKAS_SADAN = "Vikas Sadan"
VIKAS_SADAN_STATION = "Vikas Sadan Gurgaon"
VIKAS_SADAN_OUTPUT = "../../data/cron_job_data/vikas_sadan_cron_output"

stations = [(NISE,  NISE_OUTPUT), (SECTOR_51, SECTOR_51_OUTPUT), (TERI_GRAM, TERI_GRAM_OUTPUT), (VIKAS_SADAN, VIKAS_SADAN_OUTPUT)]

def get_api_token():
    try:
        return os.environ['API_TOKEN']
    except KeyError:
        print("KeyError")
         # If running locally, use an alternative method to get the API token
        return input("Enter your API token: ")
    
# Incase if api fails, write to file with previous day
# In 2nd cron daily job, Incase if api fails, write to file with previous day

def setData(station, output_file, logger, TOKEN):
    try:
        # Get the API response
        url = "https://api.waqi.info/search/?token=" + TOKEN + "&keyword=" + station
        response = requests.get(url)
        if response.status_code == 200:
            res = response.json()
            result = []
            if station.lower() in (res["data"][0]['station']['name']).lower():
                result.append(res["data"][0]['aqi'])
                result.append(res["data"][0]['station']['name'])
                result.append(pd.to_datetime(res["data"][0]['time']['stime']))
            logger.info(f"station=> {station}, result => {result}")
            print(f"{datetime.now()} - station=> {station}, result => {result}")
            
            # Write to the file only when (station, time) is not already existing in the file.

            new_timestamp = (res["data"][0]['time']['stime'])
            csv_file_path = output_file + '.csv'

            # Check if the new timestamp is already present
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                # Assuming the timestamp is in the 3rd column
                existing_timestamps = [row[2] for row in csv_reader]

            if new_timestamp not in existing_timestamps:
                with open(csv_file_path, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(result)
                print(f'The data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
                logger.info(f'{datetime.now()} - The data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
            else:
                print(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
                logger.info(f'{datetime.now()} - Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
        else:
            print(f"Error: {response.status_code} - {response.text}")
            logger.info(f"{datetime.now()} - Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception {type(e).__name__} has occured for station=> {station}")
        logger.info(f"Exception {type(e).__name__} has occured for station=> {station}")

def setLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        f"logs/{datetime.now().strftime('%d-%m-%Y')}.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)
    return logger

def writeData(station_location):
    df_api = pd.read_csv(station_location + ".csv")
    df_api['Time'] = pd.to_datetime(df_api['Time'])
    df_api.set_index('Time', inplace=True)
    df_api.resample('D').mean()
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    yesterday_aqi = df_api[yesterday:yesterday]
    print(yesterday_aqi)

if __name__ == "__main__":

    # Logging
    logger = setLogger()
    
    # Get API token
    TOKEN = get_api_token()

    for station, station_location in stations:
        setData(station,  station_location, logger, TOKEN)
    
    # If the day changes, append it to original data

#     if datetime.now().hour == 1:     # It means 1 AM
#         for station, station_location in stations:
#             writeData(station_location)