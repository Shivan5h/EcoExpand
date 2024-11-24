from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Initialize FastAPI
app = FastAPI(title="EcoExpand Risk and Incentive Analysis API", version="1.0")

# Load Data
data = pd.read_csv('market_data.csv')  # Replace with your dataset

# Preprocessing
data.dropna(inplace=True)
data['Market_Risk_Score'] = data['Political_Stability'] * 0.4 + data['Economic_Stability'] * 0.6

# Clustering for Market Risk Categorization
kmeans = KMeans(n_clusters=3, random_state=42)
data['Risk_Cluster'] = kmeans.fit_predict(data[['Market_Risk_Score']])

# Train Random Forest for Incentive Prediction
X = data[['Export_Incentives', 'Duty_Drawback', 'Trade_Agreements', 'Market_Risk_Score']]
y = data['Cost_Saving']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)


# Pydantic Models for Input Validation
class CountryRequest(BaseModel):
    country: str


class RiskResponse(BaseModel):
    country: str
    risk_cluster: str
    predicted_cost_savings: str


# API Endpoints
@app.get("/")
def root():
    return {"message": "Welcome to the EcoExpand Risk and Incentive Analysis API"}


@app.get("/countries/")
def list_countries():
    countries = data['Country'].unique().tolist()
    return {"countries": countries}


@app.post("/analyze/", response_model=RiskResponse)
def analyze_country(request: CountryRequest):
    country = request.country
    country_data = data[data['Country'] == country]

    if country_data.empty:
        raise HTTPException(status_code=404, detail=f"No data available for {country}")

    # Risk Cluster
    risk_cluster = int(country_data['Risk_Cluster'].values[0])
    risk_cluster_label = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}[risk_cluster]

    # Predict Cost Savings
    cost_saving = rf_model.predict(
        country_data[['Export_Incentives', 'Duty_Drawback', 'Trade_Agreements', 'Market_Risk_Score']])

    return RiskResponse(
        country=country,
        risk_cluster=f"Cluster {risk_cluster} ({risk_cluster_label})",
        predicted_cost_savings=f"${cost_saving[0]:,.2f}"
    )


@app.get("/feature-importance/")
def feature_importance():
    importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
    return importances.to_dict()
