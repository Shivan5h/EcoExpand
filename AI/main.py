
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import openai
import spacy
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk import download
import re
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os


app = FastAPI(title="EcoExpand AI Platform", 
             description="Unified API for compliance, risk analysis, and knowledge management",
             version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")
print("russian ka dam bad gaya hai market mai bc ")


nlp = spacy.load("en_core_web_sm")
knowledge_graph = nx.DiGraph()
stop_words = set(stopwords.words("english"))


download('punkt')
download('stopwords')


data = pd.read_csv('market_data.csv')
data.dropna(inplace=True)
data['Market_Risk_Score'] = data['Political_Stability'] * 0.4 + data['Economic_Stability'] * 0.6


kmeans = KMeans(n_clusters=3, random_state=42)
data['Risk_Cluster'] = kmeans.fit_predict(data[['Market_Risk_Score']])

X = data[['Export_Incentives', 'Duty_Drawback', 'Trade_Agreements', 'Market_Risk_Score']]
y = data['Cost_Saving']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)


class QueryRequest(BaseModel):
    user_query: str
    context: str = None

class TextInput(BaseModel):
    text: str

class CountryRequest(BaseModel):
    country: str

class RiskResponse(BaseModel):
    country: str
    risk_cluster: str
    predicted_cost_savings: str

class Entity(BaseModel):
    name: str
    type: str

class Relation(BaseModel):
    source: str
    target: str
    relation: str

class GraphData(BaseModel):
    entities: List[Entity]
    relations: List[Relation]


def generate_response(user_query: str, context: str = None) -> str:
    try:
        system_prompt = (
            "You are EcoExpand AI, a smart chatbot that helps users understand compliance regulations "
            "and international export incentives. Provide detailed, accurate, and actionable guidance."
        )
        if context:
            system_prompt += f"\nContext: {context}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def extract_key_phrases(text, top_n=10):
    doc = nlp(text)
    nouns_verbs = [token.text for token in doc if token.pos_ in ("NOUN", "VERB")]
    filtered_words = [word for word in nouns_verbs if word not in stop_words]
    return Counter(filtered_words).most_common(top_n)

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    doc = nlp(text)
    sentence_scores = {}
    
    for sent in sentences:
        words = preprocess_text(sent).split()
        for word in words:
            if word in stop_words:
                continue
            for token in doc:
                if token.text == word:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + token.rank
    
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    return " ".join(ranked_sentences[:num_sentences])




@app.get("/")
def root():
    return {"message": "Welcome to EcoExpand AI Platform! Access various services through dedicated endpoints."}


@app.post("/chat")
def chat_with_ai(query: QueryRequest):
    try:
        response = generate_response(query.user_query, query.context)
        return {"response": response}
    except HTTPException as e:
        raise e


@app.post("/extract-key-phrases")
async def get_key_phrases(input: TextInput):
    try:
        text = preprocess_text(input.text)
        key_phrases = extract_key_phrases(text)
        return {"key_phrases": key_phrases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize-text")
async def get_summary(input: TextInput):
    try:
        summary = summarize_text(input.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/countries")
def list_countries():
    countries = data['Country'].unique().tolist()
    return {"countries": countries}

@app.post("/analyze", response_model=RiskResponse)
def analyze_country(request: CountryRequest):
    country = request.country
    country_data = data[data['Country'] == country]
    
    if country_data.empty:
        raise HTTPException(status_code=404, detail=f"No data available for {country}")
    
    risk_cluster = int(country_data['Risk_Cluster'].values[0])
    risk_cluster_label = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}[risk_cluster]
    
    cost_saving = rf_model.predict(
        country_data[['Export_Incentives', 'Duty_Drawback', 'Trade_Agreements', 'Market_Risk_Score']])
    
    return RiskResponse(
        country=country,
        risk_cluster=f"Cluster {risk_cluster} ({risk_cluster_label})",
        predicted_cost_savings=f"${cost_saving[0]:,.2f}"
    )


@app.post("/add_entities")
def add_entities(entities: List[Entity]):
    for entity in entities:
        knowledge_graph.add_node(entity.name, type=entity.type)
    return {"message": f"{len(entities)} entities added successfully."}

@app.post("/add_relations")
def add_relations(relations: List[Relation]):
    for relation in relations:
        if not knowledge_graph.has_node(relation.source) or not knowledge_graph.has_node(relation.target):
            raise HTTPException(status_code=404, detail="Source or target entity not found.")
        knowledge_graph.add_edge(relation.source, relation.target, relation=relation.relation)
    return {"message": f"{len(relations)} relations added successfully."}

@app.get("/get_graph")
def get_graph():
    nodes = [{"name": node, **data} for node, data in knowledge_graph.nodes(data=True)]
    edges = [{"source": u, "target": v, "relation": data["relation"]} 
            for u, v, data in knowledge_graph.edges(data=True)]
    return {"nodes": nodes, "edges": edges}

@app.get("/visualize_graph")
def visualize_graph():
    pos = nx.spring_layout(knowledge_graph)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(knowledge_graph, pos, node_size=1500, node_color="lightblue")
    nx.draw_networkx_labels(knowledge_graph, pos, font_size=10)
    nx.draw_networkx_edges(knowledge_graph, pos, arrowstyle="->", arrowsize=20, edge_color="gray")
    edge_labels = nx.get_edge_attributes(knowledge_graph, "relation")
    nx.draw_networkx_edge_labels(knowledge_graph, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Knowledge Graph Visualization")
    plt.axis("off")
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return StreamingResponse(buf, media_type="image/png")