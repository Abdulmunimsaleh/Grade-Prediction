import joblib
import pandas as pd
import numpy
import pickle as pk
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

model1_path = 'models/Gradient_Boosting_Regression_model_1.pkl'
model2_path = 'models/Gradient_Boosting_Regression_model_2.pkl'
model3_path = 'models/Gradient_Boosting_Regression_model_3.pkl'

grade_model_path = 'models/extra_trees_model.pkl'
grade_model = joblib.load(grade_model_path)

model1 = joblib.load(model1_path)
model2 = joblib.load(model2_path)
model3 = joblib.load(model3_path)

def predictWith(choice, gpa):
    if choice == 1:
        return model1.predict([[gpa / 4]]) * 4
    if choice == 2:
        return model2.predict([[gpa / 4]]) * 4
    if choice == 3:
        return model3.predict([[gpa / 4]]) * 4

@application.route("/predictgpa/", methods=['GET'])
def gpa_results():

    gpa = request.args.get("gpa")
    print("type: ", type(gpa))
    gpa = float(gpa)
    choice = int(request.args.get("choice"))
    print("gpa: ", gpa);
    print("choice: ", choice);
    result = [0]

    if gpa != 0.0:
        result = predictWith(choice, gpa)
    print("result: ", result);

    results = {
        "gpa": abs(result[0]),
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route("/predictgrade/", methods=['GET'])
def grade_results():

    jsonData = request.args.get("data")

    # parse x:
    trial_input = json.loads(jsonData)
    df = pd.DataFrame([trial_input], columns=trial_input.keys())
    print(df)

    # model prediction here
    grade_result = class_prediction(df)

    results = {
        "grade": abs(grade_result),
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def class_prediction(inp):
    prediction = grade_model.predict(inp)
    return round(prediction[0], 2)

if __name__ == "__main__":
   application.run()