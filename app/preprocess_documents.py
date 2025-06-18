# preprocess_documents.py

import re
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download("punkt")
nltk.download("stopwords")
nlp = spacy.load("en_core_web_sm")

def preprocess_text(raw_text: str) -> str:
    # Lowercase & strip special characters
    text = re.sub(r"[^a-zA-Z\s]", "", raw_text.lower())

    # Tokenization
    tokens = word_tokenize(text)

    # Stopword removal
    stop_words = set(stopwords.words("english"))
    filtered = [w for w in tokens if w not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(w) for w in filtered]

    # Lemmatization using spaCy for better context
    doc = nlp(" ".join(stemmed))
    lemmatized = [token.lemma_ for token in doc]

    return " ".join(lemmatized)
