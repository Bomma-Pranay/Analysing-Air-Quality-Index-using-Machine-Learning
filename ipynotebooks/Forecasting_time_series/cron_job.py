import requests
import pandas as pd
import pprint
import csv
from datetime import datetime
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

def get_api_token():
    try:
        return os.environ['API_TOKEN']
    except KeyError:
        print("KeyError")
         # If running locally, use an alternative method to get the API token
        return input("Enter your API token: ")
    
# Incase if api fails, write to file with previous day
# In 2nd cron daily job, Incase if api fails, write to file with previous day

def setData(station, output_file):
    try:
        
#         # Create a "logs" directory if it doesn't exist
#         logs_directory = "../../logs"
#         os.makedirs(logs_directory, exist_ok=True)

#         # Set up logger configuration
#         log_file_path = os.path.join(logs_directory, f"{datetime.now().strftime('%d-%m-%Y')}.log")
#         logger.basicConfig(filename=log_file_path, level=logger.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        logger = logging.getLogger(__name__)

        logger.setLevel(logging.DEBUG)
        logger_file_handler = logging.handlers.RotatingFileHandler(
            f"../../logs/{datetime.now().strftime('%d-%m-%Y')}.log",
            maxBytes=1024 * 1024,
            backupCount=1,
            encoding="utf8",
        )
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logger_file_handler.setFormatter(formatter)
        logger.addHandler(logger_file_handler)
        print(f"logger {logger}" )
        
        TOKEN = get_api_token()
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
                logger.info(f'The data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
            else:
                logger.info(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
        else:
            logger.info(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print("Exception ",e)
        logger.info(f"Exception {type(e).__name__} has occured for station=> {station}")
        
# Initialize new file with ,,, or else you will get error

setData(NISE,  NISE_OUTPUT)
setData(SECTOR_51, SECTOR_51_OUTPUT)
setData(TERI_GRAM, TERI_GRAM_OUTPUT)
setData(VIKAS_SADAN, VIKAS_SADAN_OUTPUT)