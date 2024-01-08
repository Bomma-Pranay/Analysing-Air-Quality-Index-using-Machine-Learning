import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
import pickle
import datetime

app = Flask(__name__)
model = pickle.load(open('models_pickle/model_knn_date.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the AQI & Scale
    '''

    now = datetime.datetime.now()
    day = int(now.day)
    month = int(now.month)
    week = int(now.isocalendar()[1])
    hour = int(now.hour)

    PM25 = int(request.form['PM2.5'])
    NO = int(request.form['NO'])
    NO2 = int(request.form['NO2'])
    NOx = int(request.form['NOx'])
    SO2 = int(request.form['SO2'])
    CO = int(request.form['CO'])
    
    input_list = [PM25, NO, NO2, NOx, SO2, CO, day, month, week, hour]
    final_features = [np.array(input_list)]

    print(f"\n\input_list {input_list} final_features {final_features}\n\n")
    predicted_aqi = model.predict(final_features)
    predicted_aqi_scale = get_aqi_scale(predicted_aqi)
    print(f"predicted_aqi {predicted_aqi} & predicted_aqi_scale {predicted_aqi_scale}")
    
    if predicted_aqi:
        return render_template('index.html', predicted_aqi = int(predicted_aqi[0]), predicted_aqi_scale = predicted_aqi_scale, input_text_PM25 = PM25, input_text_NO = NO, input_text_NO2 = NO2, input_text_NOx = NOx, input_text_SO2 = SO2, input_text_CO = CO)

def get_aqi_scale(predicted_aqi):
    '''
    Calculate the AQI Scale
    '''

    if (predicted_aqi < 50):
        predicted_aqi_scale = 'Good'
    elif (predicted_aqi > 50 and predicted_aqi <= 100):
        predicted_aqi_scale = 'Satisfactory'
    elif (predicted_aqi > 100 and predicted_aqi <= 200):
        predicted_aqi_scale = 'Moderate'
    elif (predicted_aqi > 200 and predicted_aqi <= 300):
        predicted_aqi_scale = 'Poor'
    elif (predicted_aqi > 300 and predicted_aqi <= 400):
        predicted_aqi_scale = 'Very Poor'
    elif (predicted_aqi > 400 and predicted_aqi <= 5000):
        predicted_aqi_scale = 'Severe'
    return predicted_aqi_scale

@app.route('/Resume')
def Resume():
    return render_template('Resume.html')

if __name__ == "__main__":
    app.run(debug=True)