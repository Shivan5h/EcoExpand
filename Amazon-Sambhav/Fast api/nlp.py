from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import Counter
import re
from nltk import download

# FastAPI app initialization
app = FastAPI(title="Compliance NLP API", version="1.0")

# Download NLTK resources
download('punkt')
download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load stopwords
stop_words = set(stopwords.words("english"))


# Input schema for API
class TextInput(BaseModel):
    text: str


# Preprocessing function
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.lower()


# Function to extract key phrases
def extract_key_phrases(text, top_n=10):
    doc = nlp(text)
    nouns_verbs = [token.text for token in doc if token.pos_ in ("NOUN", "VERB")]
    filtered_words = [word for word in nouns_verbs if word not in stop_words]
    return Counter(filtered_words).most_common(top_n)


# Function to summarize text
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


# Function to extract actionable insights
def extract_actionable_insights(text):
    insights = []
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("ORG", "GPE", "MONEY", "LAW", "DATE"):
            insights.append({"text": ent.text, "type": ent.label_})
    return insights


# API endpoint for extracting key phrases
@app.post("/extract-key-phrases")
async def get_key_phrases(input: TextInput):
    try:
        text = preprocess_text(input.text)
        key_phrases = extract_key_phrases(text)
        return {"key_phrases": key_phrases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API endpoint for summarizing text
@app.post("/summarize-text")
async def get_summary(input: TextInput):
    try:
        summary = summarize_text(input.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API endpoint for extracting actionable insights
@app.post("/extract-insights")
async def get_insights(input: TextInput):
    try:
        insights = extract_actionable_insights(input.text)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
