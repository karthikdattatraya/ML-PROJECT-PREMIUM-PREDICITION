import streamlit as st
from prediction_helper import predict

st.title("Health Insurance Prediction App")


categorical_columns = {
"gender": ['Male', 'Female'],
"region": ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
"marital_status": ['Unmarried', 'Married'],
"bmi_category": ['Normal', 'Obesity', 'Overweight', 'Underweight'],
"smoking_status": ['Regular', 'No Smoking', 'Occasional'],
"employment_status": ['Salaried', 'Self-Employed', 'Freelancer'],
"income_level": ['<10L', '10L - 25L', '> 40L', '25L - 40L'],
"medical_history": ['Diabetes', 'High blood pressure', 'No Disease',
                    'Diabetes & High blood pressure', 'Thyroid', 'Heart disease',
                    'High blood pressure & Heart disease', 'Diabetes & Thyroid',
                    'Diabetes & Heart disease'],
"insurance_plan": ['Bronze', 'Silver', 'Gold']
 }

#create four rows of three columns each
row1=st.columns(3)
row2=st.columns(3)
row3=st.columns(3)
row4=st.columns(3)

# Assign inputs to the grid
with row1[0]:
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
with row1[1]:
    number_of_dependants = st.number_input("Number of Dependants", min_value=0, max_value=20, step=1)
with row1[2]:
    income_lakhs = st.number_input("Income in Lakhs", min_value=0, max_value=200, step=1)

with row2[0]:
    genetical_risk = st.number_input("Genetical Risk", min_value=0, max_value=5, step=1)
with row2[1]:
    insurance_plan = st.selectbox("Insurance Plan", categorical_columns["insurance_plan"])
with row2[2]:
    employment_status = st.selectbox("Employment Status", categorical_columns["employment_status"])

with row3[0]:
    gender = st.selectbox("Gender", categorical_columns["gender"])
with row3[1]:
    marital_status = st.selectbox("Marital Status", categorical_columns["marital_status"])
with row3[2]:
    bmi_category = st.selectbox("BMI Category", categorical_columns["bmi_category"])

with row4[0]:
    smoking_status = st.selectbox("Smoking Status", categorical_columns["smoking_status"])
with row4[1]:
    region = st.selectbox("Region", categorical_columns["region"])
with row4[2]:
    medical_history = st.selectbox("Medical History", categorical_columns["medical_history"])


#number inputs
input_dict = {
    "age": age,
    "gender": gender,
    "region": region,
    "marital_status": marital_status,
    "number_of_dependants": number_of_dependants,
    "bmi_category": bmi_category,
    "smoking_status": smoking_status,
    "employment_status": employment_status,
    "income_lakhs": income_lakhs,
    "medical_history": medical_history,
    "insurance_plan": insurance_plan,
    "genetical_risk": genetical_risk
}



if st.button("Predict"):
    prediction=predict(input_dict)
    st.success(f"Prediction Premium: {prediction}")