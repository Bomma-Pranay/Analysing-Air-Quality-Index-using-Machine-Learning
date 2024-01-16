# Project 1: AirCast

- **Designed & Developed** a website featuring integration with a **SARIMAX** model trained on Gurugram’s historical daily time series Air Quality Index data that retrains daily by a Cron job with new data and **forecasts next 5 day’s AQI**.
- Collected **3.5 years** of historical data from **CPCB**. Pre-processed data using Pandas & performed Data Analysis using Seaborn.
- Automated the process through a **GitHub Actions-enabled Cron Job** running every hour, leveraging real-time API call to assimilate new hourly AQI data and **retrain the model daily** at 1 AM.
- Deployed on **Netlify** and triggered auto-deployment. Implemented logging and exception handling for debugging and error tracking.
- **Future ideas:** Expanding to other 5+ major Indian cities and integrating with a relational database for scalability.
- **Link: http://aircastaqi.netlify.app**

# Architecture & more...

- ### The Story:
  - After completing the AQI Calculator project in May 2023, an idea sprouted in my brain - "We have the advantage of live data, can we make use of it and re-train the model every day to forecast AQI?"
  - Then, I started learning about Time Series forecasting & started this project.
  - Here, it is reverse engineering - I got the idea first, then I learned the required skills & then did the project.
- ### Input & Output: Input is the historical daily AQI data & the output is the next 5 days AQI forecast.
- ### Algorithm: SARIMAX (1, 0, 1), (1, 0, 1, 7)
- ### Data collected from: CPCB
- ### Dataset type & frequency: Daily Time Series data
- ### Dataset size: 1369 rows x 10 columns (2020-03-05 to 2023-11-23)
- ### Model metrics:
  - Mean Absolute Percentage Error (MAPE): 13.14
  - Mean Absolute Error (MAE): 36
  - Note: These are not the daily Cron job metrics, but at the time of training for the first time on the historical data. Cron job metrics are reported to the logs folder in GitHub.
- ### Timelines: November 2023 - January 2024
- ### Tech stack: Python, Time Series Analysis & Forecasting Algorithms, Flask, Pandas, Matplotlib, Seaborn, GitHub Actions
- ### Future ideas:
  - Expanding to other 5+ major Indian cities and integrating with a relational database for scalability.
