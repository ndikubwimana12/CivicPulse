from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

AGENCY_KEYWORDS = {
    'water': "water outage, no water, leak, burst pipe, drinking water",
    'road': "potholes, road broken, bridge damage, traffic",
    'health': "hospital, clinic, ambulance, medicine, health issue",
    'power': "power cut, electricity, blackout, transformer",
}

def classify_ticket(message):
    categories = list(AGENCY_KEYWORDS.keys())
    corpus = list(AGENCY_KEYWORDS.values())

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus + [message])

    similarity = cosine_similarity(tfidf[-1], tfidf[:-1])
    best_match_index = similarity.argmax()

    return categories[best_match_index]
