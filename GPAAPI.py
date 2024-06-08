import joblib
import pandas as pd
import numpy
from flask import Flask, request, jsonify
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

model1_path = 'models/Gradient_Boosting_Regression_model_1.pkl'
model2_path = 'models/Gradient_Boosting_Regression_model_2.pkl'
model3_path = 'models/Gradient_Boosting_Regression_model_3.pkl'

model1 = joblib.load(model1_path)
model2 = joblib.load(model2_path)
model3 = joblib.load(model3_path)

def predictWith(choice, gpa):
    return 2.3

@application.route("/predict/", methods=['GET'])
def get_results():

    gpa = float(request.args.get("gpa"))
    choice = int(request.args.get("choice"))
    result = None

    print("trial_input: ", trial_input);
    print("choice: ", choice);

    result = predictWith(choice, gpa);

    results = {
        "gpa": abs(result),
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
   application.run()