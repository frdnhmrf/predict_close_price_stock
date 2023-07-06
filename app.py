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

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + "eyJraWQiOiIyMDIzMDYxMDA4MzIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02NjUwMDNENllQIiwiaWQiOiJJQk1pZC02NjUwMDNENllQIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNGYxMGI5OGMtMjUyNS00NjM2LTg5YzAtODAwNTdiMjlmMmQyIiwiaWRlbnRpZmllciI6IjY2NTAwM0Q2WVAiLCJnaXZlbl9uYW1lIjoiRmVyZGlhbiBIdXNuYWwiLCJmYW1pbHlfbmFtZSI6Ik1hJ3J1ZiIsIm5hbWUiOiJGZXJkaWFuIEh1c25hbCBNYSdydWYiLCJlbWFpbCI6IjExMjIwMjAwNjUxN0BtaHMuZGludXMuYWMuaWQiLCJzdWIiOiIxMTIyMDIwMDY1MTdAbWhzLmRpbnVzLmFjLmlkIiwiYXV0aG4iOnsic3ViIjoiMTEyMjAyMDA2NTE3QG1ocy5kaW51cy5hYy5pZCIsImlhbV9pZCI6IklCTWlkLTY2NTAwM0Q2WVAiLCJuYW1lIjoiRmVyZGlhbiBIdXNuYWwgTWEncnVmIiwiZ2l2ZW5fbmFtZSI6IkZlcmRpYW4gSHVzbmFsIiwiZmFtaWx5X25hbWUiOiJNYSdydWYiLCJlbWFpbCI6IjExMjIwMjAwNjUxN0BtaHMuZGludXMuYWMuaWQifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiNjZjOTFjZjQ5Yjk1NDI1YTg2YjUxMGVjNDA5Y2JjOTciLCJpbXNfdXNlcl9pZCI6IjEwODI0ODM5IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyNjM0MjUzIn0sImlhdCI6MTY4ODY2MDEyMiwiZXhwIjoxNjg4NjYzNzIyLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MiwiYW1yIjpbIm1mYSIsIm90cCIsInB3ZCJdfQ.WleV1VMfRXyWsBP_GbFgLmyjB0lvJtgD4xvdfU2UAVE4fEZ27KjLawaPD1oqi1i3WYwUn3K0rA2Os7THmXRNDrTsxUVrB4Sli9qxV9JuNxb9qWkOtxzsTrETpyY7h4A0Cru9hV80RhP2WrQv6W8EUskaKLxhWrQjZb6g48UrUKyMIEKbvG82oYXZeDp1OyF_otPZIzdpF4i_85W7s-MeYSe7bGp3vgYYgbYLFevKXKiDmeZnz5Kj43AxzZpRPAGozy8HmjNH3RXMbnhDYeQTvWiZUuODFvGeBaJWbsqppNWEOZ8-9e0v0ZzGLm98Ek1NSL-aD079m6UIsu-DUr04tA"}
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
