import pandas as pd
from joblib import load

model_rest = load("artifacts\\model_rest.joblib")
model_young = load("artifacts\\model_young.joblib")

scaler_rest = load("artifacts\\scaler_rest.joblib")
scaler_young = load("artifacts\\scaler_young.joblib")

def calculate_normalised_score(medical_history):
    risk_score = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    diseases = medical_history.lower().split("&")
    total_risk_score = sum(risk_score.get(disease, 0) for disease in diseases)
    max_score = 14
    min_score = 0
    normalised_score = (total_risk_score - min_score) / (max_score - min_score)
    return normalised_score

def preprocess_input(input_dict):

    expected_columns = [
        'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan',
        'genetical_risk', 'normalized_score', 'gender_Male', 'region_Northwest',
        'region_Southeast', 'region_Southwest', 'marital_status_Unmarried',
        'bmi_category_Obesity', 'bmi_category_Overweight',
        'bmi_category_Underweight', 'smoking_status_Occasional',
        'smoking_status_Regular', 'employment_status_Salaried',
        'employment_status_Self-Employed'
    ]

    insurance_plan_encoding = {"Bronze": 1, "Gold": 3, "Silver": 2}

    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    for key, value in input_dict.items():

        if key == "age":
            df["age"] = value
        elif key == "number_of_dependants":
            df["number_of_dependants"] = value
        elif key == "income_lakhs":
            df["income_lakhs"] = value
        elif key == "genetical_risk":
            df["genetical_risk"] = value
        elif key == "insurance_plan":
            df["insurance_plan"] = insurance_plan_encoding.get(value, 1)

        elif key == "gender" and value == "Male":
            df["gender_Male"] = 1

        elif key == "region":
            if value == "Northwest":
                df["region_Northwest"] = 1
            elif value == "Southeast":
                df["region_Southeast"] = 1
            elif value == "Southwest":
                df["region_Southwest"] = 1

        elif key == "marital_status"and value == "Unmarried":
            df["marital_status_Unmarried"] = 1  #drop 1st is true so no hard encoding

        elif key == "bmi_category":
            if value == "Obesity":
                df["bmi_category_Obesity"] = 1
            elif value == "Overweight":
                df["bmi_category_Overweight"] = 1
            elif value == "Underweight":
                df["bmi_category_Underweight"] = 1

        elif key == "smoking_status":
            if value == "Occasional":
                df["smoking_status_Occasional"] = 1
            elif value == "Regular":
                df["smoking_status_Regular"] = 1

        elif key == "employment_status":
            if value == "Salaried":
                df["employment_status_Salaried"] = 1
            elif value == "Self-Employed":
                df["employment_status_Self-Employed"] = 1
    df["normalized_score"] = calculate_normalised_score(input_dict["medical_history"])
    df = handle_scaling(int(input_dict["age"]), df)
    return df

def handle_scaling(age, df): #age=int(input_dict["age"]) alredy converted it into an integer
    if age <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    columns_to_scale = scaler_object["cols_to_scale"]
    scaler = scaler_object["scaler"]

    df["income_level"] = None
    df[columns_to_scale] = scaler.transform(df[columns_to_scale])
    df.drop("income_level", axis="columns", inplace=True)
    return df

def predict(input_dict):
    input_dict = preprocess_input(input_dict)

    if int(input_dict["age"])<= 25:
        prediction = model_young.predict(input_dict)
    else:
        prediction = model_rest.predict(input_dict)

    return int(prediction[0])


