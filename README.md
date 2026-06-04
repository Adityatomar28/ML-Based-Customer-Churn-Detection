# 📡 ML-Based-Customer-Churn-Detection


![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Random%20Forest-orange?logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow?logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green)

> Predict customer churn risk in real time using machine learning and behavioral analytics — with an interactive dark-themed dashboard, live model inference, and AI-generated retention recommendations.

---

## 🖥️ Live Dashboard Preview

| Churn Predictor | Analytics Hub |
|---|---|
<img width="453" height="697" alt="Screenshot 2026-06-05 at 12 12 38 AM" src="https://github.com/user-attachments/assets/3fb319ad-d67b-46cb-9416-67dd3076ec9a" />


---

## ✨ Features

- 🔮 **Real-time churn prediction** — enter customer details and get an instant churn risk score
- 📊 **Global Analytics Hub** — churn distribution, monthly charges, contract type, and retention by tenure
- 💡 **AI Loyalty Recommendations** — actionable retention strategies generated per customer profile
- 🧠 **Model Explainability** — top feature importance drivers shown for every prediction
- 🟢 **Production Model Status** — live indicator showing model is online and serving

---

## 📁 Folder Structure

```
ML-Based-Customer-Churn-Detection/
│
├── static/
│   ├── css/                   # Stylesheets
│   └── js/                    # Frontend JavaScript
│
├── templates/
│   └── index.html             # Main dashboard UI
│
├── notebooks/
│   ├── 01_EDA.ipynb           # Exploratory Data Analysis
│   ├── 02_Data_Preprocessing.ipynb
│   └── 03_Model_Training.ipynb
│
├── churnapp.py                # Flask app — routes & ML inference
├── app.js                     # Frontend logic
├── churn_dataset.csv          # Raw dataset
├── churn_model.pkl            # Trained Random Forest model
├── churn_model1.pkl           # Alternate model checkpoint
├── requirements.txt
└── README.md
```

---

## 📊 Key Stats (from Dashboard)

| Metric | Value |
|---|---|
| Total Customers | 7,032 |
| Active Customers | 5,163 |
| Churn Rate | 26.58% |
| Model Accuracy | **77% (Random Forest)** |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ML & Data | Python, Pandas, NumPy, Scikit-learn |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Visualization | Chart.js / custom JS charts |
| Model Persistence | Joblib (`.pkl`) |
| Version Control | Git & GitHub |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ML-Based-Customer-Churn-Detection.git
cd ML-Based-Customer-Churn-Detection
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python churnapp.py
```

### 5. Open in browser
```
http://localhost:5001
```

---

## 🤖 How the Prediction Works

1. User enters customer details (gender, contract type, services, charges, tenure)
2. Flask backend preprocesses inputs and runs inference via the trained Random Forest model
3. Dashboard displays:
   - **Churn Risk %** (e.g. 53.3% = HIGH RISK)
   - **Top feature drivers** explaining the prediction
   - **Loyalty Recommendations** tailored to the customer profile

---

## 📈 Model Building Summary

- **Task:** Binary Classification (`Churn` = Yes / No)
- **Train/Test Split:** 75% / 25%
- **Preprocessing:** One-hot encoding for categorical features, normalization for numerical
- **Models Evaluated:**

| Model | Notes |
|---|---|
| K-Nearest Neighbors | Baseline |
| Logistic Regression | Interpretable |
| Support Vector Machine | High-dimensional |
| Decision Tree | Explainable |
| **Random Forest** ✅ | **Best accuracy — selected for production** |

---

## 📉 Key Churn Insights (from EDA)

- Customers on **month-to-month contracts** churn the most
- **Higher monthly charges** strongly correlate with churn
- **Short tenure** (0–12 months) has the lowest retention rate
- Customers **without tech support or online security** are at higher risk
- **Two-year contract** customers have near-zero churn

---

## 💡 Business Recommendations

1. **Offer contract upgrade incentives** — 15% discount for switching to a 12-month plan
2. **Proactive loyalty credits** — apply $10/month credit for high-billing customers
3. **Bundle premium support** — include free tech support tier for at-risk customers
4. **Target new customers early** — first 12 months are the highest churn risk window

---

## 🔮 Future Enhancements

- [ ] Add XGBoost / LightGBM for improved accuracy
- [ ] Integrate Customer Lifetime Value (CLV) scoring
- [ ] Add SHAP-based explainability (full waterfall charts)
- [ ] User authentication for multi-team access
- [ ] Export predictions as CSV for CRM integration

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ for production-grade customer analytics.
