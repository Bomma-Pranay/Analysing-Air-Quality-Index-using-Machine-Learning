import numpy as np
from flask import Flask, request, jsonify, render_template
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
    For rendering results on HTML GUI
    '''

    now = datetime.datetime.now()
    day = int(now.day)
    month = int(now.month)
    week = int(now.isocalendar()[1])
    hour = int(now.hour)

    # Sample prediction
    # model.predict([[283, 0, 0, 32, 0, 0, day, month, week, hour]])
    print(f"request {request}")
    print(f"\n\nrequest.form {request.form} \n\nrequest.form.values {request.form.values()} ")

    PM25 = float(request.form['PM2.5'])
    NO = float(request.form['NO'])
    NO2 = float(request.form['NO2'])
    NOx = float(request.form['NOx'])
    SO2 = float(request.form['SO2'])
    CO = float(request.form['CO'])
    
    input_list = [PM25, NO, NO2, NOx, SO2, CO, day, month, week, hour]
    print(input_list)
    
    # int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(input_list)]
    print(f"\n\input_list {input_list} final_features {final_features}\n\n")
    predicted_aqi = model.predict(final_features)
    print(f"predicted_aqi {predicted_aqi}")

    predicted_aqi_scale = get_aqi_scale(predicted_aqi)

    if predicted_aqi:
        return render_template('index.html', predicted_aqi=predicted_aqi[0], predicted_aqi_scale = predicted_aqi_scale)

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

def get_aqi_scale(predicted_aqi):
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

if __name__ == "__main__":
    app.run(debug=True)