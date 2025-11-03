#!/usr/bin/env python
import joblib
import sys
from features import extract_features

model = joblib.load("model/rf_phishing.pkl")

def predict(url):
    features = extract_features(url)
    prob = model.predict_proba([features])[0][1]
    label = "PHISHING" if prob > 0.5 else "SAFE"
    return label, prob

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    label, prob = predict(url)
    print(f"{label} ({prob:.1%})")
