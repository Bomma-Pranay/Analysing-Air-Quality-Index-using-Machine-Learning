import requests
import pprint
import csv
from datetime import datetime, timedelta
import logging
import os
import logging.handlers

# Data analysis
import pandas as pd 

# Data Visualization
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px 

# Time Series
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA 
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
import statsmodels.api as sm

# For printing multiple outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Visualization parameters
sns.set(rc={"figure.dpi":100, 'savefig.dpi':300})
sns.set_context('notebook')
sns.set_style("ticks")
from IPython.display import set_matplotlib_formats
%config InlineBackend.figure_format = 'retina'

# NISE
NISE = "nise gwal"
NISE_STATION = "NISE Gwal Pahari, Gurugram, India"
NISE_OUTPUT = "data/cron_job_data/nise_cron_output"

# Sector 51
SECTOR_51 = "Sector-51, Gurugram"
SECTOR_51_STATION = "Sector-51, Gurugram, India"
SECTOR_51_OUTPUT = "data/cron_job_data/sector_51_cron_output"
SECTOR_51_DAILY_AQI = 'data/cleaned_data/Forecasting_time_series/sector_51_daily_aqi.csv'

# Teri gram
TERI_GRAM = "Teri Gram"
TERI_GRAM_STATION = "Teri Gram, Gurugram"
TERI_GRAM_OUTPUT = "data/cron_job_data/teri_gram_cron_output"

# Vikas Sadan
VIKAS_SADAN = "Vikas Sadan"
VIKAS_SADAN_STATION = "Vikas Sadan Gurgaon"
VIKAS_SADAN_OUTPUT = "data/cron_job_data/vikas_sadan_cron_output"

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
            print(f"station=> {station}, result => {result}")
            
            # If AQI is not a number, dont write it and return
            try:
                int(result[0])
            except Exception as exception:
                logger.info(f"AQI is not an integer. Exception {type(exception).__name__} has occured for station=> {station}")
                return
            
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
                logger.info(f'The data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
            else:
                print(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
                logger.info(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
        else:
            print(f"Error: {response.status_code} - {response.text}")
            logger.info(f"Error: {response.status_code} - {response.text}")
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

def writeData(station_hourly_aqi, station_daily_aqi):
    df_api = pd.read_csv(station_hourly_aqi + ".csv")
    df_api['Time'] = pd.to_datetime(df_api['Time'])
    df_api.set_index('Time', inplace=True)
    df_api = df_api['AQI'].resample('D').mean()
    df_api = pd.DataFrame(df_api)
    print(f"df_api columns {df_api.columns}")
    df_api['AQI'] = round(df_api['AQI'])
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    temp_daily_aqi = pd.read_csv(station_daily_aqi)
    print(f'temp_daily_aqi columns {temp_daily_aqi.columns}')
    temp_daily_aqi['Date'] = pd.to_datetime(temp_daily_aqi['Date'])
    temp_daily_aqi.set_index('Date', inplace=True)

    print(f"temp_daily_aqi[{yesterday}]=> {temp_daily_aqi[yesterday:yesterday]}")
    with open(station_daily_aqi, 'a', newline='') as csv_file:
        if len(temp_daily_aqi[yesterday:yesterday]) == 0: # Write only if it does not exist already
            csv_writer = csv.writer(csv_file)    
            csv_writer.writerow([temp_daily_aqi.iloc[-1,0] + 1, yesterday, df_api[yesterday:yesterday].AQI.values[0]])

if __name__ == "__main__":

    # Logging
    logger = setLogger()
    
    # Get API token
    TOKEN = get_api_token()

    for station, station_location in stations:
        setData(station,  station_location, logger, TOKEN)
    
     # If the day changes, append it to original data
    
    if datetime.now().hour == 20:     # It means 1 AM IST (20 is GitHub action runner time)
        writeData(SECTOR_51_OUTPUT, SECTOR_51_DAILY_AQI)
#         for station, station_location in stations:
#             writeData(station_location)