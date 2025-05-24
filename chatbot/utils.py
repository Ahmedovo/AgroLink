import os
import json
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from pathlib import Path
# Get the base directory of your Django project (where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define absolute paths
TRAINING_FILE = os.path.join(BASE_DIR, 'chatbot','data', 'training_data.json')
MODEL_FILE = os.path.join(BASE_DIR, 'chatbot','data', 'trained_model.pkl')
VECTORIZER_FILE = os.path.join(BASE_DIR,'chatbot', 'data', 'vectorizer.pkl')

def train_bot():
    if not os.path.exists(MODEL_FILE):
        print("Training ML model...")
        with open(TRAINING_FILE, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
        
        questions = list(training_data.keys())
        answers = list(training_data.values())

        df = pd.DataFrame({'question': questions, 'answer': answers})

        # Vectorize text
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['question'])
        y = df['answer']

        # Train model
        model = LogisticRegression()
        model.fit(X, y)

        # Save model + vectorizer
        joblib.dump(model, MODEL_FILE)
        joblib.dump(vectorizer, VECTORIZER_FILE)
        print("Model trained and saved.")
    else:
        print("ML model already exists. Skipping training.")

def get_bot_response(user_message):
    if not os.path.exists(MODEL_FILE) or not os.path.exists(VECTORIZER_FILE):
        train_bot()

    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)

    X_user = vectorizer.transform([user_message])
    prediction = model.predict(X_user)[0]
    
    return prediction
