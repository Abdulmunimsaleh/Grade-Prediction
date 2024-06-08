import pandas as pd
import joblib

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

first_year, first_two_years, first_three_years
print(len(first_three_years))

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

def display_menu(model, course_grades):
    columns = course_grades
    my_grades = ["BA", "AA", "0", "BB", "DD", "FD", "FF", "DC", "CC", "AA", "BA", "BB"]
    
    # for i in columns:
    #     my_grades.append("AA")

    print("my_grades: ", my_grades)
    prediction_input = pd.DataFrame([my_grades], columns=columns)
    prediction_input = encode_data(prediction_input)
    print("prediction_input: ", prediction_input)
    print("The predicted CGPA is:", model.predict(prediction_input))

print("="*124)
print("\t\t\t\t\t\tWELCOME TO CGPA PREDICTOR")
print("="*124)
print("\t\t\tTHIS MODEL CAN PREDICT THE FINAL CGPA OF A STUDENT AT THE END OF FOURTH YEAR\n \t\t\t\tGIVEN GPs OF THE COURSES OBTAINED IN FIRST THREE YEARS")
print("*"*124)

choice = int(input("Please select one of the following options:\n\
    1. Predict CGPA based on GPs of First Year\n\
    2. Predict CGPA based on GPs of First Two Years\n\
    3. Predict CGPA based on GPs of First Three Years\n"))
print("="*124)


if choice == 1:
    display_menu(reg1, first_year)
elif choice == 2:
    display_menu(grad2, first_two_years)
elif choice == 3:
    display_menu(grad3, first_three_years)
else:
    print("Please select valid choice")
