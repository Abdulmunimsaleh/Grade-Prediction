import joblib
import pandas as pd
import pickle as pk
import json
import sklearn
from flask import Flask, request, jsonify
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

# Load model here
model_path = 'models/extra_trees_model.pkl'
loaded_model = joblib.load(model_path)

def class_prediction(inp):

    prediction = loaded_model.predict(inp)
    return round(prediction[0], 2)

@application.route("/predict/", methods=['GET'])
def get_results():

    jsonData = request.args.get("data")

    # parse x:
    trial_input = json.loads(jsonData)
    df = pd.DataFrame([trial_input], columns=trial_input.keys())
    print(df)

    # model prediction here
    grade_result = class_prediction(df)

    results = {
        "grade": grade_result,
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
   application.run()