import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="AI Telecom Churn Prediction",
    page_icon="📡",
    layout="centered"
)

st.title("📡 AI Telecom Customer Churn Prediction")
st.markdown("Predict customer churn risk using machine learning and behavioral analytics.")

st.subheader("Customer Information")

# Categorical Dropdowns and Toggles
gender = st.selectbox("Gender", ["Female", "Male"])
senior_citizen_label = st.selectbox("Senior Citizen (Aged 65 or older)", ["No", "Yes"])
phone_service_label = st.selectbox("Phone Service", ["Yes", "No"])

# Handle dependent fields gracefully
if phone_service_label == "No":
    multiple_lines_label = "No phone service"
    st.info("Multiple Lines is set to 'No phone service' because Phone Service is No.")
else:
    multiple_lines_label = st.selectbox("Multiple Lines", ["No", "Yes"])

streaming_tv_label = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
streaming_movies_label = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
paperless_billing_label = st.selectbox("Paperless Billing", ["Yes", "No"])

st.subheader("Billing Information")
monthly_charges = st.slider("Monthly Charges ($)", min_value=18.25, max_value=118.75, value=50.00, step=0.25)
total_charges = st.number_input("Total Charges ($)", min_value=18.80, max_value=8684.80, value=150.00, step=0.01)

# Encodings
gender_encoded = 0 if gender == "Female" else 1
senior_citizen_encoded = 1 if senior_citizen_label == "Yes" else 0
phone_service_encoded = 1 if phone_service_label == "Yes" else 0

if multiple_lines_label == "Yes":
    multiple_lines_encoded = 2
elif multiple_lines_label == "No phone service":
    multiple_lines_encoded = 1
else:
    multiple_lines_encoded = 0

if streaming_tv_label == "Yes":
    streaming_tv_encoded = 2
elif streaming_tv_label == "No internet service":
    streaming_tv_encoded = 1
else:
    streaming_tv_encoded = 0

if streaming_movies_label == "Yes":
    streaming_movies_encoded = 2
elif streaming_movies_label == "No internet service":
    streaming_movies_encoded = 1
else:
    streaming_movies_encoded = 0

paperless_billing_encoded = 1 if paperless_billing_label == "Yes" else 0

btn_click = st.button("Predict Churn", type="primary")

# Load model
try:
    with open("churn_model1.pkl", "rb") as f:
        model = joblib.load(f)
    model_loaded = True
except Exception as e:
    st.error(f"Error loading model: {e}")
    model_loaded = False

if btn_click and model_loaded:
    # Order: ['gender', 'SeniorCitizen', 'PhoneService', 'MultipleLines', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling', 'MonthlyCharges', 'TotalCharges']
    features = np.array([[
        gender_encoded,
        senior_citizen_encoded,
        phone_service_encoded,
        multiple_lines_encoded,
        streaming_tv_encoded,
        streaming_movies_encoded,
        paperless_billing_encoded,
        float(monthly_charges),
        float(total_charges)
    ]]).reshape(1, -1)
    
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    churn_prob = probabilities[1] * 100
    retained_prob = probabilities[0] * 100
    
    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ **High Churn Risk!**")
        st.metric(label="Churn Probability", value=f"{churn_prob:.1f}%")
        st.write("### Recommended Retention Actions:")
        st.write("- **Contract Lock-in:** Offer a 15% discount for a 12-month agreement extension.")
        st.write("- **Proactive Discount:** Apply a $10/month loyalty credit for 6 months.")
        st.write("- **Priority Care:** Assign account to a premium support team.")
    else:
        st.success(f"✅ **Low Churn Risk (Loyal Customer)**")
        st.metric(label="Retention Score", value=f"{retained_prob:.1f}%")
        st.write("### Recommended Account Actions:")
        st.write("- **Value Expansion:** Offer a special bundle on streaming service upgrades.")
        st.write("- **Payment rewards:** Incentivize auto-pay signups with a $5 billing credit.")
