from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key'  # you will need a secret key

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


@app.route('/', methods=('GET', 'POST'))
def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)


@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        API_KEY = "H8rNaZmjBcpsjtRYf-zVtAvHYcUM4TILAmKXZJg6V7xw"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                         API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        imtoken = token_response.json()["access_token"]

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + imtoken, }
        python_object = ["", float(form.open.data), float(form.high.data),
                         float(form.low.data), float(0), int(form.volume.data)]
        # Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [
            {"fields": ["Date", "Open", "High", "Low", "Adj Close", "Volume"], "values": userInput}]}
        response_scoring = requests.post(
            "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ddd28081-ccc4-497e-a147-9b062bb0d4c6/predictions?version=2021-05-01", json=payload_scoring, headers=header)

        output = response_scoring.text
        json_output = json.loads(output)
        for key in json_output:
            prediction = json_output[key]

        for key in prediction[0]:
            values = prediction[0][key]

        form.close = values[0][0]
        return render_template('index.html', form=form)


@app.route('/time', methods=('GET', 'POST'))
def predicttime():
    form = PredictForm()
    if form.submit():

        # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        API_KEY = "H8rNaZmjBcpsjtRYf-zVtAvHYcUM4TILAmKXZJg6V7xw"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                         API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        imtoken = token_response.json()["access_token"]

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + imtoken, }
        python_object1 = [form.date1.data]
        python_object2 = [form.date2.data]
        python_object3 = [form.date3.data]
        python_object4 = [form.date4.data]
        python_object5 = [form.date5.data]
        # Transform python objects to  Json

        userInput = []
        userInput.append(python_object1)
        userInput.append(python_object2)
        userInput.append(python_object3)
        userInput.append(python_object4)
        userInput.append(python_object5)
        print(userInput)
        print("====================================")

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [
            {"fields": ["Date", "Open", "High", "Low", "Adj Close", "Volume"], "values": userInput}]}
        response_scoring = requests.post(
            "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ddd28081-ccc4-497e-a147-9b062bb0d4c6/predictions?version=2021-05-01", json=payload_scoring, headers=header)
        print(payload_scoring)
        print("====================================")
        output = response_scoring.text
        print(output)
        json_output = json.loads(output)
        for key in json_output:
            prediction = json_output[key]

        for key in prediction[0]:
            values = prediction[0][key]

        form.close_date_1 = values[0][0]
        form.close_date_2 = values[1][0]
        form.close_date_3 = values[2][0]
        form.close_date_4 = values[3][0]
        form.close_date_5 = values[4][0]
        return render_template('index.html', form=form)
