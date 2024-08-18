import requests
import csv
from datetime import datetime, timedelta
import logging
import os
import logging.handlers

# Data analysis
import pandas as pd
import numpy as np

# Time Series
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA 
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Metrics for model evaluation
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

# NISE
NISE = "nise gwal"
NISE_STATION = "NISE Gwal Pahari, Gurugram, India"
NISE_OUTPUT = "data/cron_job_data/nise_cron_output"

# Sector 51
SECTOR_51 = "Sector-51, Gurugram"
SECTOR_51_STATION = "Sector-51, Gurugram, India"
SECTOR_51_OUTPUT = "data/cron_job_data/sector_51_cron_output"
SECTOR_51_OUTPUT_FLASK = "static/data/sector_51_cron_output"
SECTOR_51_DAILY_AQI = 'data/cleaned_data/Forecasting_time_series/sector_51_daily_aqi.csv'
SECTOR_51_DAILY_AQI_FLASK = 'static/data/sector_51_daily_aqi.csv'

# Teri gram
TERI_GRAM = "Teri Gram"
TERI_GRAM_STATION = "Teri Gram, Gurugram"
TERI_GRAM_OUTPUT = "data/cron_job_data/teri_gram_cron_output"

# Vikas Sadan
VIKAS_SADAN = "Vikas Sadan"
VIKAS_SADAN_STATION = "Vikas Sadan Gurgaon"
VIKAS_SADAN_OUTPUT = "data/cron_job_data/vikas_sadan_cron_output"

# stations = [(NISE,  NISE_OUTPUT), (SECTOR_51, SECTOR_51_OUTPUT), (SECTOR_51, SECTOR_51_OUTPUT_FLASK), (TERI_GRAM, TERI_GRAM_OUTPUT), (VIKAS_SADAN, VIKAS_SADAN_OUTPUT)]
stations = [(SECTOR_51, SECTOR_51_OUTPUT), (SECTOR_51, SECTOR_51_OUTPUT_FLASK)]

# We have selected best model based on different combinations - See Modelling block in ipython notebook.
ORDER, SEASONAL_ORDER = (1, 0, 1), (1, 0, 1, 7)
FORECAST_SECTOR_51_DAILY_AQI = 'data/cleaned_data/Forecasting_time_series/forecast_sector_51_daily_aqi.csv'
FORECAST_SECTOR_51_DAILY_AQI_FLASK = 'static/data/forecast_sector_51_daily_aqi.csv'

def get_api_token():
    '''
    This function fetches the AQI token.
    '''
    try:
        return os.environ['API_TOKEN']
    except KeyError:
        print("KeyError")
         # If running locally, use an alternative method to get the API token
        return input("Enter your API token: ")
    
def setData(station, output_file, logger, TOKEN):
    '''
    This function is called hourly once. 
    It fetches the real-time hourly AQI data for 4 stations and writes to the hourly csv files.
    This data is consumed by writeData function.
    '''
    
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
            
            # If AQI is not a number, dont write it and return
            try:
                int(result[0])
            except Exception as exception:
                # logger.info(f"setData function - AQI is not an integer. Exception {type(exception).__name__} has occured for station=> {station}")
                print(f"setData function - AQI is not an integer. Exception {type(exception).__name__} has occured for station=> {station}")
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
                logger.info(f"station=> {station}, result => {result}")
                print(f"station=> {station}, result => {result}")
                print(f'The hourly data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
                logger.info(f'The hourly data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
            else:
                print(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
            #     logger.info(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
        else:
            print(f"setData function - Error: {response.status_code} - {response.text}")
            logger.info(f"setData function - Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"setData function - Exception {type(e).__name__} has occured for station=> {station}")
        logger.info(f"setData function - Exception {type(e).__name__} has occured for station=> {station}")

def setLogger():
    '''
    This function sets the logger to the logs directory.
    Every day, a new file gets created.
    '''
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
    '''
    This function is called daily once at 1 AM. 
    It preprocesses the data, computes the daily AQI from hourly AQI csv files and writes to the daily csv files.
    This data is consumed by retrain_model function.
    '''
    # Hourly data preprocessing
    df_api = pd.read_csv(station_hourly_aqi + ".csv")
    df_api['Time'] = pd.to_datetime(df_api['Time'])
    df_api.set_index('Time', inplace=True)
    df_api = df_api['AQI'].resample('D').mean()
    df_api = pd.DataFrame(df_api)
    print(f"df_api columns {df_api.columns}")
    logger.info(f"df_api columns {df_api.columns}")
    df_api['AQI'] = round(df_api['AQI'])

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    print(f'today=> {today} & yesterday=> {yesterday}')
    logger.info(f'today=> {today} & yesterday=> {yesterday}')

    # Write it to the Daily data csv file
    temp_daily_aqi = pd.read_csv(station_daily_aqi)
    print(f'temp_daily_aqi columns {temp_daily_aqi.columns}')
    logger.info(f'temp_daily_aqi columns {temp_daily_aqi.columns}')
                
    temp_daily_aqi['Date'] = pd.to_datetime(temp_daily_aqi['Date'])
    temp_daily_aqi.set_index('Date', inplace=True)

    print(f"temp_daily_aqi[{yesterday}]=> {temp_daily_aqi[yesterday:yesterday]}")
    logger.info(f"temp_daily_aqi[{yesterday}]=> {temp_daily_aqi[yesterday:yesterday]}")
    
    try:
        with open(station_daily_aqi, 'a', newline='') as csv_file:
            if len(temp_daily_aqi[yesterday:yesterday]) == 0: # Write only if it does not exist already
                csv_writer = csv.writer(csv_file)
                index = temp_daily_aqi.iloc[-1,0] + 1 # Add 1 to yesterday's index
                aqi = df_api[yesterday:yesterday].AQI.values[0]
                print(f'Index => {index}, yesterday => {yesterday} & AQI => {aqi}')
                logger.info(f'Index => {index}, yesterday => {yesterday} & AQI => {aqi}')
                if np.isnan(df_api[yesterday:yesterday].AQI.values[0]): # If NaN, take yesterday's value.
                    aqi = temp_daily_aqi.iloc[-1,1]
                csv_writer.writerow([index, yesterday, aqi])
                print(f'Daily AQI data has been written to {station_daily_aqi}')
                logger.info(f'Daily AQI data has been written to {station_daily_aqi}')
        
        # Also, write to Flask app
        with open(SECTOR_51_DAILY_AQI_FLASK, 'a', newline='') as csv_file:
            if len(temp_daily_aqi[yesterday:yesterday]) == 0: # Write only if it does not exist already
                csv_writer = csv.writer(csv_file)
                index = temp_daily_aqi.iloc[-1,0] + 1 # Add 1 to yesterday's index
                aqi = df_api[yesterday:yesterday].AQI.values[0]
                print(f'Index => {index}, yesterday => {yesterday} & AQI => {aqi}')
                logger.info(f'Index => {index}, yesterday => {yesterday} & AQI => {aqi}')
                if np.isnan(df_api[yesterday:yesterday].AQI.values[0]): # If NaN, take yesterday's value.
                    aqi = temp_daily_aqi.iloc[-1,1]
                csv_writer.writerow([index, yesterday, aqi])
                print(f'Daily AQI data has been written to {SECTOR_51_DAILY_AQI_FLASK}')
                logger.info(f'Daily AQI data has been written to {SECTOR_51_DAILY_AQI_FLASK}')
    except Exception as e:
        print(f"writeData function - Exception {type(e).__name__} has occured for station=> {station_daily_aqi}")
        logger.info(f"writeData function - Exception {type(e).__name__} has occured for station=> {station_daily_aqi}")

def retrain_model(order, seasonal_order, station_daily_aqi):
    '''
    This function is called daily once at 1 AM. 
    It takes into account today's AQI and re-trains the model.
    We check the model's performance by splitting data into train & test data, then train the model and calculate MAPE.
    We consider entire data (no splitting into train & test) and re-train our model & forecast for the next 5 days.
    '''

    # Read the data & clean it.
    daily_aqi = pd.read_csv(station_daily_aqi)
    daily_aqi['Date'] = pd.to_datetime(daily_aqi['Date'])
    daily_aqi.set_index('Date', inplace=True)
    daily_aqi.drop(columns=['Unnamed: 0'], inplace=True)
    daily_aqi.index = pd.to_datetime(daily_aqi.index)
    daily_aqi.ffill(inplace=True)

    df = daily_aqi
    
    # Split into train & test
    train_end = df.index[-1] - timedelta(days=5)  # Except last 5 days
    print(f"train_end=> {train_end}")
    logger.info(f'Re-training the model & train_end is {train_end}')
    
    train_data = df.loc[:train_end, 'AQI']
    test_data = df.loc[train_end + timedelta(days=1):, 'AQI']

    # Train the model
    model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()

    predictions = model_fit.forecast(len(test_data))
    predictions = pd.Series(predictions, index=test_data.index)
    
    # Calculate MAPE
    MAPE = round(mean_absolute_percentage_error(test_data, predictions) * 100, 2)  # Round it off to two decimal points
    print(f"\n\nMAPE=> {MAPE}")
    logger.info(f'Retrained the model & MAPE is {MAPE}%')

    # Calculate MAE
    MAE = mean_absolute_error(test_data, predictions)
    print(f"\n\nMAE=> {MAE}")
    logger.info(f'Retrained the model & MAE is {MAE}')

    train_data = df.loc[:, 'AQI']
    model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()
    predictions = model_fit.forecast(len(test_data))
    predictions = pd.Series(predictions)
    print(f"\n\nForecast=> {predictions}")
    logger.info(f"Forecast=> {predictions}")

    # Save the forecast
    try:
        containsNaN = predictions.isna().sum()
        if containsNaN == 0:
            with open(FORECAST_SECTOR_51_DAILY_AQI, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Date', 'AQI'])
                for i in range(5):
                    csv_writer.writerow([predictions.index[i].date(), round(predictions.values[i])])
                # Log the predictions to view in future.
                print(f'The forecast data has been written to {FORECAST_SECTOR_51_DAILY_AQI}')
                logger.info(f'The forecast data has been written to {FORECAST_SECTOR_51_DAILY_AQI}')
            
            # Also, write to Flask app
            with open(FORECAST_SECTOR_51_DAILY_AQI_FLASK, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Date', 'AQI'])
                for i in range(5):
                    csv_writer.writerow([predictions.index[i].date(), round(predictions.values[i])])
                # Log the predictions to view in future.
                print(f'The forecast data has been written to {FORECAST_SECTOR_51_DAILY_AQI_FLASK}')
                logger.info(f'The forecast data has been written to {FORECAST_SECTOR_51_DAILY_AQI_FLASK}')
        else:
            print(f'retrain_model function - The forecast data has NaNs.')
            logger.info(f'retrain_model function - The forecast data has NaNs.')
    
    except Exception as e:
        print(f"retrain_model function - Model is not retrained. Please look into the issue - Exception {type(e).__name__} has occured.")
        logger.info(f"retrain_model function - Model is not retrained. Please look into the issue - Exception {type(e).__name__} has occured.")

if __name__ == "__main__":

    # Logging
    logger = setLogger()
    
    # Get API token
    TOKEN = get_api_token()

    for station, station_location in stations:
        setData(station,  station_location, logger, TOKEN)
    
     # If the day changes, append it to original data
    print(f"datetime.now()=> {datetime.now()}")
    # logger.info(f"datetime.now()=> {datetime.now()}")
    
    daily_AQI = pd.read_csv(SECTOR_51_DAILY_AQI)
    daily_AQI['Time'] = pd.to_datetime(daily_AQI['Date'])
    daily_AQI.set_index('Time', inplace=True)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    yesterday_present = daily_AQI.index[-1] == pd.Timestamp(yesterday)

    if (not yesterday_present) or (datetime.now().hour == 1):     # It means 1 AM IST (20 is GitHub action runner time)
        print(f"Calling writeData & retrain_model functions. Time => {datetime.now().hour} | yesterday_present=> {yesterday_present} ")
        logger.info("Calling writeData & retrain_model functions. Time=> ",datetime.now().hour, "yesterday_present => ",yesterday_present)
        writeData(SECTOR_51_OUTPUT, SECTOR_51_DAILY_AQI)
        retrain_model(ORDER, SEASONAL_ORDER, SECTOR_51_DAILY_AQI)
#         for station, station_location in stations:
#             writeData(station_location)
    # response = requests.get("https://AQI-Calculator.onrender.com")
    # print(f"response.status_code {response.status_code}")
