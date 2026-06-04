import streamlit as st
import pandas as pd
import numpy as np
import sklearn
import joblib

st.title("Churn Prediction App")
st.subheader("Enter the feature details to predict")

gender= st.text_input("Enter the gender")
SeniorCitizen= st.text_input("Enter the SeniorCitizen")
PhoneService= st.text_input("Enter the PhoneService")
MultipleLines= st.text_input("Enter the MultipleLines")
StreamingTV= st.text_input("Enter the StreamingTV")
StreamingMovies= st.text_input("Enter the StreamingMovies")
PaperlessBilling= st.text_input("Enter the PaperlessBilling")
MonthlyCharges= st.text_input("Enter the MonthlyCharges")
TotalCharges= st.text_input("Enter the TotalCharges")

btn_click = st.button("Predict")

with open("churn_model1.pkl", "rb") as f:
    model = joblib.load(f)

if btn_click == True:
    features = np.array([[float(gender),float(SeniorCitizen),float(PhoneService),
    float(MultipleLines),float(StreamingTV),float(StreamingMovies),float(PaperlessBilling),
    float(MonthlyCharges),float(TotalCharges)]]).reshape(1,-1)
    output = model.predict(features)
    st.write("The prediction is ",output)




