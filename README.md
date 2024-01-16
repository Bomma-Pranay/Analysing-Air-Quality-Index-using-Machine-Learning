# Project 1: AirCast

- **Designed & Developed** a website featuring integration with a **SARIMAX** model trained on Gurugram’s historical daily time series Air Quality Index data that retrains daily by a Cron job with new data and **forecasts next 5 day’s AQI**.
- Collected **3.5 years** of historical data from **[CPCB](https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing)**. Pre-processed data using Pandas & performed Data Analysis using Seaborn.
- Automated the process through a **GitHub Actions-enabled Cron Job** running every hour, leveraging real-time API call to assimilate new hourly AQI data and **retrain the model daily** at 1 AM.
- Deployed on **Netlify** and triggered auto-deployment. Implemented logging and exception handling for debugging and error tracking.
- **Future ideas:** Expanding to other 5+ major Indian cities and integrating with a relational database for scalability.
- **Link: http://AirCastAQI.netlify.app**

![AirCast Website](https://github.com/Bomma-Pranay/Analysing-Air-Quality-Index-using-Machine-Learning/assets/62324691/837cce45-3ac7-4a5a-90c8-b8210dec9edd)

## Architecture & more...
![AirCast Architecture PNG](https://github.com/Bomma-Pranay/Analysing-Air-Quality-Index-using-Machine-Learning/assets/62324691/0c4d7662-4d3b-4f51-bf7c-6bd94459bbfe)

- **The Story:**
  - After completing the AQI Calculator project in May 2023, an idea sprouted in my brain - "We have the advantage of live data, can we make use of it and re-train the model every day to forecast AQI?"
  - Then, I started learning about Time Series forecasting & started this project.
  - Here, it is reverse engineering - I got the idea first, then I learned the required skills & then did the project.
- **Input & Output:** Input is the historical daily AQI data & the output is the next 5 days AQI forecast.
- **Algorithm:** SARIMAX (1, 0, 1), (1, 0, 1, 7)
- **Data collected from:** **[CPCB](https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing)**
- **Dataset type & frequency:** Daily Time Series data
- **Dataset size:** 1369 rows x 10 columns (2020-03-05 to 2023-11-23)
- **Model metrics:**
  - Mean Absolute Percentage Error (MAPE): 13.14
  - Mean Absolute Error (MAE): 36
  - Note: These are not the daily Cron job metrics, but at the time of training for the first time on the historical data. Cron job metrics are reported to the logs folder in GitHub.
- **Timelines:** November 2023 - January 2024
- **Tech stack:** Python, Time Series Analysis & Forecasting Algorithms, Flask, Pandas, Matplotlib, Seaborn, GitHub Actions
- **Future ideas:**
  - Expanding to other 5+ major Indian cities and integrating with a relational database for scalability.

---

# Project 2: AQI Calculator
- Trained a predictive model using **kNN algorithm** to predict **Air Quality Index (AQI)** based on input pollutants, attained **83.5% accuracy (R-squared)** on 147,000+ data points from 4 **Gurugram** stations.
- Spearheaded a multi-national team of 5 at **[Omdena](https://www.omdena.com/projects/analyzing-air-quality-in-gurugram-using-machine-learning)**, managing data collection, EDA, model training, & documentation.
- Collected & compiled hourly data for 4 stations in Gurugram from **[CPCB](https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing)**.
- **Resolved 30% of missing values** using appropriate imputation techniques by performing comprehensive EDA using Pandas, Matplotlib, and Seaborn.
- Exported the best kNN model using **Pickle** & deployed **Flask app on Render** for real-time AQI prediction.
- **Link: https://AQI-Calculator.onrender.com/**
  
![AQI Calculator Website](https://github.com/Bomma-Pranay/Analysing-Air-Quality-Index-using-Machine-Learning/assets/62324691/f02c2056-e2e3-4310-8aff-c2ef8959e4e2)

- **Documentation:**: https://docs.google.com/document/d/1-wDKgZj5Ex0wCB2Qte3kWNOCw189PQTXl2EUiyUBHxg/edit?usp=sharing
  
## Architecture & more...
![AQI_Calculator Architecture PNG](https://github.com/Bomma-Pranay/Analysing-Air-Quality-Index-using-Machine-Learning/assets/62324691/ed32a56d-bcb5-4cac-8ccc-d740a84cf1cc)

- **The Story:**
  - After learning the concepts of ML, writing blogs/posts, and hustling on Kaggle, I wanted to build my first end-to-end project that too with a good team & environment. So, I joined Omdena & started this project.
  - Here, I learned the skills first, then did the project.
- **Input & Output:** Given pollutants as input to the Machine Learning model, predict the Air Quality Index.
- Collaborated with Omdena, worked with people across the globe, and led a team of 5 people in Data Collection, Exploratory Data Analysis, Model Training & Project Documentation.
- **Algorithm:** k Nearest Neighbors (k = 5)
- **Data collected from:** **[CPCB](https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing)**
- **Dataset type & frequency:** Hourly Time Series data with target column as AQI
- **Dataset size:** 147531 rows x 31 columns
- **Model metrics:**
  - R-Squared: 0.835
  - Mean Absolute Percentage Error (MAPE): 21.06
  - Mean Absolute Error (MAE): 30.75
- **Timelines:** March 2023 - May 2023
- **Tech stack:** Python, Pandas, Scikit-learn, Matplotlib, Seaborn, Plotly, Flask
