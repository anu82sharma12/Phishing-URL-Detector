#!/usr/bin/env python

import os
import pandas as pd
import joblib
import urllib.request
import zipfile
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from features import extract_features

MODEL_DIR = "model"
DATA_DIR = "data"
MODEL_PATH = f"{MODEL_DIR}/rf_phishing.pkl"

def ensure_dirs():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

def download_sample_data():
    print("Downloading sample phishing + legit URLs...")
    urls = [
        ("https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-links.txt", "phishing.txt"),
        ("https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-domains.txt", "domains.txt"),
        ("https://raw.githubusercontent.com/martenson/disposable-email-domains/master/disposable_email_blocklist.conf", "blocklist.txt"),
    ]
    for url, fname in urls:
        path = f"{DATA_DIR}/{fname}"
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
            print(f"   {fname}")

    # Generate CSV
    phish_urls = [line.strip() for line in open(f"{DATA_DIR}/ALL-phishing-links.txt") if line.strip()][:5000]
    legit_urls = [
        "https://github.com", "https://google.com", "https://stackoverflow.com",
        "https://wikipedia.org", "https://python.org"
    ] * 1000

    pd.DataFrame(phish_urls, columns=["url"]).to_csv(f"{DATA_DIR}/phishing.csv", index=False)
    pd.DataFrame(legit_urls, columns=["url"]).to_csv(f"{DATA_DIR}/legit.csv", index=False)
    print("Sample data ready → data/")

def train_and_save():
    print("Training model on 10,000 URLs...")
    phish = pd.read_csv(f"{DATA_DIR}/phishing.csv")["url"].tolist()
    legit = pd.read_csv(f"{DATA_DIR}/legit.csv")["url"].tolist()

    X = [extract_features(u) for u in phish + legit]
    y = [1] * len(phish) + [0] * len(legit)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"Accuracy: {acc:.1%}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved → {MODEL_PATH} ({os.path.getsize(MODEL_PATH)/1e6:.1f} MB)")

if __name__ == "__main__":
    print("Phishing Detector Setup")
    ensure_dirs()
    if not os.path.exists(MODEL_PATH):
        download_sample_data()
        train_and_save()
    else:
        print(f"Model already exists: {MODEL_PATH}")
    print("\nSetup complete! Run:\n   python detector.py 'https://g00gle-login.com'")
