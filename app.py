import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load the model
MODEL_PATH = "churn_model1.pkl"
DATASET_PATH = "churn_dataset.csv"

model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"Model not found at {MODEL_PATH}")

# Load and clean dataset for analytics
df_clean = None
if os.path.exists(DATASET_PATH):
    try:
        df = pd.read_csv(DATASET_PATH)
        # Clean TotalCharges (same as preprocessing)
        df_clean = df.copy()
        df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'].replace(" ", np.nan), errors='coerce')
        df_clean = df_clean.dropna(subset=['TotalCharges'])
        print(f"Dataset loaded and cleaned. Shape: {df_clean.shape}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
else:
    print(f"Dataset not found at {DATASET_PATH}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    if df_clean is None:
        return jsonify({"error": "Dataset not loaded"}), 500
    
    # 1. Summary KPIs
    total_customers = int(df_clean.shape[0])
    churned_customers = int((df_clean['Churn'] == 'Yes').sum())
    retained_customers = total_customers - churned_customers
    churn_rate = round((churned_customers / total_customers) * 100, 2)
    
    # 2. Churn Distribution
    churn_dist = {
        "labels": ["Active (Retained)", "Churned"],
        "values": [retained_customers, churned_customers]
    }
    
    # 3. Monthly Charges Distribution
    # Bins: 0-20, 20-40, 40-60, 60-80, 80-100, 100-120
    bins = [0, 20, 40, 60, 80, 100, 120]
    bin_labels = ["$0-20", "$20-40", "$40-60", "$60-80", "$80-100", "$100-120"]
    
    df_clean['MonthlyChargesBin'] = pd.cut(df_clean['MonthlyCharges'], bins=bins, labels=bin_labels)
    charges_retained = df_clean[df_clean['Churn'] == 'No'].groupby('MonthlyChargesBin', observed=False).size().tolist()
    charges_churned = df_clean[df_clean['Churn'] == 'Yes'].groupby('MonthlyChargesBin', observed=False).size().tolist()
    
    monthly_charges_dist = {
        "labels": bin_labels,
        "retained": charges_retained,
        "churned": charges_churned
    }
    
    # 4. Contract Type vs Churn
    contract_retained = df_clean[df_clean['Churn'] == 'No'].groupby('Contract', observed=False).size().to_dict()
    contract_churned = df_clean[df_clean['Churn'] == 'Yes'].groupby('Contract', observed=False).size().to_dict()
    
    contracts = ["Month-to-month", "One year", "Two year"]
    contract_dist = {
        "categories": contracts,
        "retained": [int(contract_retained.get(c, 0)) for c in contracts],
        "churned": [int(contract_churned.get(c, 0)) for c in contracts]
    }
    
    # 5. Customer Retention Trends (Tenure cohorts vs Churn Rate)
    # Bins: 0-12m, 12-24m, 24-36m, 36-48m, 48-60m, 60-72m
    tenure_bins = [0, 12, 24, 36, 48, 60, 72]
    tenure_labels = ["0-12m", "12-24m", "24-36m", "36-48m", "48-60m", "60-72m"]
    df_clean['TenureBin'] = pd.cut(df_clean['tenure'], bins=tenure_bins, labels=tenure_labels)
    
    tenure_counts = df_clean.groupby('TenureBin', observed=False).size()
    tenure_churned = df_clean[df_clean['Churn'] == 'Yes'].groupby('TenureBin', observed=False).size()
    
    retention_rates = []
    for label in tenure_labels:
        total = tenure_counts.get(label, 0)
        churned = tenure_churned.get(label, 0)
        if total > 0:
            rate = round(((total - churned) / total) * 100, 1)
        else:
            rate = 100.0
        retention_rates.append(rate)
        
    retention_trends = {
        "labels": tenure_labels,
        "retentionRates": retention_rates
    }
    
    # 6. Model Feature Importances (pre-extracted from inspecting the model)
    feature_importances = {
        "labels": [
            "Monthly Charges",
            "Total Charges",
            "Senior Citizen",
            "Paperless Billing",
            "Streaming Movies",
            "Streaming TV",
            "Multiple Lines",
            "Gender",
            "Phone Service"
        ],
        "values": [33.84, 32.20, 9.37, 6.85, 5.11, 4.68, 4.57, 2.47, 0.92]
    }
    
    return jsonify({
        "summary": {
            "totalCustomers": total_customers,
            "activeCustomers": retained_customers,
            "churnRate": churn_rate,
            "modelAccuracy": 77.0
        },
        "churnDistribution": churn_dist,
        "monthlyCharges": monthly_charges_dist,
        "contractChurn": contract_dist,
        "retentionTrends": retention_trends,
        "featureImportances": feature_importances
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
        
    try:
        data = request.get_json()
        
        # Extract features
        gender_raw = data.get("gender", "Female") # Female or Male
        senior_citizen = int(data.get("SeniorCitizen", 0)) # 0 or 1
        phone_service_raw = data.get("PhoneService", "Yes") # Yes or No
        multiple_lines_raw = data.get("MultipleLines", "No") # Yes, No, or No phone service
        streaming_tv_raw = data.get("StreamingTV", "No") # Yes, No, or No internet service
        streaming_movies_raw = data.get("StreamingMovies", "No") # Yes, No, or No internet service
        paperless_billing_raw = data.get("PaperlessBilling", "Yes") # Yes or No
        monthly_charges = float(data.get("MonthlyCharges", 50.0))
        total_charges = float(data.get("TotalCharges", 50.0))
        
        # Encodings
        gender = 0 if gender_raw == "Female" else 1
        phone_service = 1 if phone_service_raw == "Yes" else 0
        
        if multiple_lines_raw == "Yes":
            multiple_lines = 2
        elif multiple_lines_raw == "No phone service":
            multiple_lines = 1
        else:
            multiple_lines = 0
            
        # UI toggles might just map to Yes/No, so we handle standard inputs or No internet service
        if streaming_tv_raw == "Yes":
            streaming_tv = 2
        elif streaming_tv_raw == "No internet service":
            streaming_tv = 1
        else:
            streaming_tv = 0
            
        if streaming_movies_raw == "Yes":
            streaming_movies = 2
        elif streaming_movies_raw == "No internet service":
            streaming_movies = 1
        else:
            streaming_movies = 0
            
        paperless_billing = 1 if paperless_billing_raw == "Yes" else 0
        
        # Create feature array
        features = np.array([[
            gender,
            senior_citizen,
            phone_service,
            multiple_lines,
            streaming_tv,
            streaming_movies,
            paperless_billing,
            monthly_charges,
            total_charges
        ]]).reshape(1, -1)
        
        # Run prediction
        churn_pred = model.predict(features)[0]
        churn_prob = model.predict_proba(features)[0]
        
        churn_probability = float(churn_prob[1]) # probability of Churn (class 1)
        retained_probability = float(churn_prob[0]) # probability of Retain (class 0)
        
        # Risk Score (0-100)
        risk_score = round(churn_probability * 100, 1)
        retention_score = round(retained_probability * 100, 1)
        
        will_churn = bool(churn_pred == 1)
        
        # Identify top risk / strength factors
        factors = []
        recommendations = []
        
        if will_churn:
            # Risk Factors
            if monthly_charges > 75:
                factors.append({
                    "name": "High Monthly Charges",
                    "impact": "High Risk",
                    "description": f"Monthly billing of ${monthly_charges} is above average tier."
                })
            if paperless_billing == 1:
                factors.append({
                    "name": "Paperless Billing Active",
                    "impact": "Medium Risk",
                    "description": "Paperless customers show higher transition rates."
                })
            if streaming_tv == 2 or streaming_movies == 2:
                factors.append({
                    "name": "High Streaming Usage",
                    "impact": "Medium Risk",
                    "description": "Subscribed to streaming content, causing billing spikes."
                })
            if senior_citizen == 1:
                factors.append({
                    "name": "Senior Citizen Account",
                    "impact": "Medium Risk",
                    "description": "Demographic segment shows higher sensitivity to billing changes."
                })
            
            # Default fallback factor if empty
            if not factors:
                factors.append({
                    "name": "Contract Status",
                    "impact": "Medium Risk",
                    "description": "Month-to-month contracts are highly prone to churn."
                })
                
            # Retention recommendations
            recommendations = [
                {"action": "Transition to 1 or 2-Year Contract", "detail": "Offer a 15% discount on monthly charges if customer signs a 12-month agreement."},
                {"action": "Proactive Loyalty Discount", "detail": "Apply a $10 monthly credit for the next 6 months to offset high billing risk."},
                {"action": "Premium Tech Support bundle", "detail": "Include a free premium customer support tier to build relationship value."}
            ]
        else:
            # Strength Factors (Loyalty)
            if monthly_charges <= 45:
                factors.append({
                    "name": "Low Billing Cost",
                    "impact": "High Loyalty",
                    "description": "Low monthly charges represent a cost-effective utility plan."
                })
            if phone_service == 1 and multiple_lines == 2:
                factors.append({
                    "name": "Multiple Phone Lines",
                    "impact": "High Loyalty",
                    "description": "Multi-line configuration increases account stickiness."
                })
            if senior_citizen == 0:
                factors.append({
                    "name": "Standard Account Segment",
                    "impact": "Low Risk",
                    "description": "Low baseline churn probability for this demographic."
                })
            
            if not factors:
                factors.append({
                    "name": "Steady Payment Behavior",
                    "impact": "Low Risk",
                    "description": "Stable usage and billing charges align with high retention profiles."
                })
                
            recommendations = [
                {"action": "Upsell Streaming bundle", "detail": "Offer a special bundle of Streaming TV & Movies with a 3-month trial."},
                {"action": "Enroll in Auto-Pay Reward", "detail": "Provide a one-time $5 billing credit for enrolling in Auto-Pay."},
                {"action": "Send Customer Appreciation Note", "detail": "Send personalized email with account value summary and a loyalty thank-you."}
            ]
            
        return jsonify({
            "churn": will_churn,
            "probability": risk_score if will_churn else retention_score,
            "riskScore": risk_score,
            "retentionScore": retention_score,
            "factors": factors,
            "recommendations": recommendations
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Run on port 5001 to avoid conflict with macOS AirPlay (on 5000)
    app.run(host='0.0.0.0', port=5001, debug=True)