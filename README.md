# telecom-churn-prediction
Link of the problem statement
https://docs.google.com/document/d/1zhMqoDYlv1iB7u-NaojanYK_e6nsQP1xMidN0CFtxc0/edit?usp=sharing

# Telecom Customer Churn Prediction

This project presents a comprehensive analysis and predictive modeling solution to address the challenge of customer churn in the telecommunications industry. The work is structured into three main phases: exploratory data analysis (EDA), development of an interactive data dashboard, and machine learning model building. Each sprint is designed to contribute to a robust understanding of customer behavior and enable actionable business decisions for reducing churn and enhancing customer retention.

## Sprint 1: Exploratory Data Analysis

The initial phase of the project focuses on a detailed exploratory data analysis (EDA) to understand the patterns and characteristics of customer data. We examined the distribution of all variables, including customer demographics, service usage patterns, and account details. Key visualizations such as histograms, boxplots, and correlation matrices were used to identify trends and anomalies. One of the most significant findings was that customers with short tenure, high monthly charges, and month-to-month contracts were more likely to churn. Additionally, customers without internet services like tech support or online security exhibited higher churn rates. These insights suggest that service bundling and incentives for long-term contracts could help reduce churn. The EDA provided crucial input for feature selection in the later modeling stage.

## Sprint 2: Interactive Dashboard Using Streamlit

To communicate our findings effectively and interactively, we developed a data dashboard using Streamlit. The dashboard allows end users to explore churn trends across various customer segments by applying filters based on contract type, payment method, service subscriptions, and other demographics. Users can instantly see how these features influence churn, with charts updating dynamically based on their selections. This interactive experience empowers business stakeholders to make data-driven decisions in real time. The Streamlit dashboard offers a modern alternative to traditional slide decks, providing a professional and engaging interface for both internal analysis and client presentations.

## Sprint 3: Model Building and Prediction

The final sprint involved preparing the data and building predictive models to classify whether a customer is likely to churn. After identifying the task as a binary classification problem, we selected "Churn" as the target variable and applied standard preprocessing techniques. Numerical variables were normalized, and categorical variables were one-hot encoded. The dataset was split into training and testing sets using a 75:25 ratio. We trained multiple models including K-Nearest Neighbors, Logistic Regression, Support Vector Machines, Decision Trees, and Random Forest. Each model was evaluated using accuracy as the primary metric. Among all the algorithms, the Random Forest classifier achieved the highest accuracy and was selected as the final model for deployment. The results were visualized in a comparison plot to clearly show model performance.

## Conclusion and Recommendations

This end-to-end telecom churn prediction solution offers powerful insights and a practical toolset for reducing customer turnover. From the EDA, we learned which customer characteristics are most indicative of churn. The Streamlit dashboard enables business users to interact with this information and explore trends without technical expertise. The final machine learning model provides a reliable method to identify at-risk customers in advance, allowing for timely interventions. We recommend deploying the Random Forest model into a live environment where it can evaluate incoming customer data and flag high-risk individuals for retention campaigns. Additionally, future enhancements could include integrating customer lifetime value metrics and exploring advanced ensemble methods like XGBoost for further performance gains.

## Technologies Used

The project was implemented using Python and key data science libraries including Pandas, NumPy, Scikit-learn, Matplotlib, and Seaborn. Streamlit was used to develop the interactive dashboard. Git and GitHub were used for version control and collaboration.

## How to Run the Project

1. Clone the repository to your local machine.
2. Install required dependencies using `pip install -r requirements.txt`.
3. Run the Jupyter notebooks in order for EDA and modeling.
4. To launch the dashboard, execute `streamlit run app.py`.

This project provides a strong foundation for predictive customer analytics in the telecom sector and can be extended or adapted to similar challenges in other subscription-based industries.

