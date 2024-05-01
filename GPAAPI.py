import joblib
import pandas as pd
import numpy
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

prediction_input = pd.DataFrame()

pd.set_option('future.no_silent_downcasting', True)
df = pd.read_csv("cgpa-dataset.csv")
df = df.drop(["SeAt No.", "ECC403", "ECC426", "ECC421", "ECC412", "ECC413", "ECC415", "COM490", "COM491"], axis=1)
df = df.drop(df[df.isnull().sum(axis=1) >= 23].index)
df = df.fillna(0)

grade_points = { 
    "FF":  1.0, "FD":  2.0,
    "DD": 2.4,  "DC": 2.7,
    "DC":  3.0, "CC": 3.4,
    "CB": 3.7,  "BB":  4.0,
    "BA": 4.4,  "BA": 4.7,
    "AA":  5.0, "AA": 5.0 
}

df = df.replace({"WU":"F", "I":"F", "W":"0"})
df = df.replace(grade_points)
X = df.drop("CGPA", axis=1)

columns = df.columns.to_list()
first_year, first_two_years = [],[]
for i in columns:
    if i[3] == '1':
        first_year.append(i)
        first_two_years.append(i)
    elif i[3] == '2':
        first_two_years.append(i)

first_three_years = list(X.columns)

model1_path = 'models/model1_linear_regression.pkl'
model2_path = 'models/model2_gradient_boosting.pkl'
model3_path = 'models/model3_gradient_boosting.pkl'

reg1 = joblib.load(model1_path)
grad2 = joblib.load(model2_path)
grad3 = joblib.load(model3_path)

def encode_data(input_df):
    df = input_df.fillna(0)
    df = df.replace({"WU":"FF", "I":"FF", "W":"0"})
    df = df.replace(grade_points)
    return df

prediction_input = pd.DataFrame()

def display_menu(model, grading_type, course_grades):
    prediction_input = pd.DataFrame([course_grades], columns=grading_type)
    prediction_input = encode_data(prediction_input)
    return model.predict(prediction_input)

def extract(variable):

    value = variable

    print("...", type(value));

    while(type(value) == numpy.ndarray):
        value = value[0]

    return value

@application.route("/predict/", methods=['GET'])
def get_results():

    jsonData = request.args.get("data")
    choice = int(request.args.get("choice"))
    result = None

    trial_input = json.loads(jsonData)

    print("trial_input: ", trial_input);
    print("choice: ", choice);

    if choice == 1:
        result = display_menu(reg1, first_year, trial_input)
    elif choice == 2:
        result = display_menu(grad2, first_two_years, trial_input)
    elif choice == 3:
        result = display_menu(grad3, first_three_years, trial_input)
    # else:
    #     # throw error

    newResult = extract(result);

    print("hello: ", extract(result));

    results = {
        "gpa": newResult,
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
   application.run()