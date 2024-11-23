import spacy
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import download
from collections import Counter
import re

# Download NLTK resources
download('punkt')
download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load stopwords
stop_words = set(stopwords.words("english"))

# Function to preprocess text
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
            insights.append((ent.text, ent.label_))
    return insights

# Example usage
if __name__ == "__main__":
    # Sample regulatory text
    regulatory_text = """
    Businesses exporting sustainable products to the US must comply with the Trade Facilitation Agreement (TFA).
    Incentives include a 10% reduction in duties under RoDTEP for eligible goods and duty drawbacks for exported materials.
    EU regulations require compliance with REACH standards and documentation of supply chain sustainability. Exporters may apply for tax incentives.
    """
    
    regulatory_text = preprocess_text(regulatory_text)

    print("Key Phrases:")
    print(extract_key_phrases(regulatory_text))

    print("\nSummary:")
    print(summarize_text(regulatory_text))

    print("\nActionable Insights:")
    print(extract_actionable_insights(regulatory_text))
