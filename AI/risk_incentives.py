import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('market_data.csv')  # Replace with your file containing market and incentive data

# Preprocessing
data.dropna(inplace=True)  # Remove rows with missing values
data['Market_Risk_Score'] = data['Political_Stability'] * 0.4 + data['Economic_Stability'] * 0.6

# Clustering for Market Risk Categorization
kmeans = KMeans(n_clusters=3, random_state=42)
data['Risk_Cluster'] = kmeans.fit_predict(data[['Market_Risk_Score']])

# Display clusters
print("Cluster Centroids:", kmeans.cluster_centers_)
print(data[['Country', 'Market_Risk_Score', 'Risk_Cluster']].head())

# Incentive Analysis using Random Forest
# Target Variable: Cost Savings; Features: Incentive Availability and Market Factors
X = data[['Export_Incentives', 'Duty_Drawback', 'Trade_Agreements', 'Market_Risk_Score']]
y = data['Cost_Saving']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict and Evaluate
y_pred = rf_model.predict(X_test)
print(f"Model Accuracy (R^2 Score): {rf_model.score(X_test, y_test):.2f}")

# Feature Importance
feature_importance = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("Feature Importance:\n", feature_importance)

# Visualize Feature Importance
feature_importance.plot(kind='bar', title='Feature Importance')
plt.show()

# Final Analysis Results
def analyze_country_risks(data, country):
    country_data = data[data['Country'] == country]
    if country_data.empty:
        return f"No data available for {country}."
    
    risk_cluster = country_data['Risk_Cluster'].values[0]
    cost_saving = rf_model.predict(country_data[['Export_Incentives', 'Duty_Drawback', 'Trade_Agreements', 'Market_Risk_Score']])
    
    return {
        "Country": country,
        "Risk Cluster": f"Cluster {risk_cluster} (0: Low Risk, 1: Medium Risk, 2: High Risk)",
        "Predicted Cost Savings": f"${cost_saving[0]:,.2f}",
    }

# Example Analysis
country_analysis = analyze_country_risks(data, "India")
print("Country Analysis:\n", country_analysis)
