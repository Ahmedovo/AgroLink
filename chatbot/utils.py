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
    # Vérifier d'abord les questions spécifiques à l'agriculture
    if "vendre" in user_message.lower():
        return get_sales_advice(user_message)
    elif "arrosage" in user_message.lower() or "irrigation" in user_message.lower():
        return get_irrigation_advice(user_message)
    elif "vache" in user_message.lower() or "lait" in user_message.lower():
        return get_cattle_advice(user_message)
    
    # Si aucune correspondance spécifique, utiliser le modèle ML
    if not os.path.exists(MODEL_FILE) or not os.path.exists(VECTORIZER_FILE):
        train_bot()

    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)

    X_user = vectorizer.transform([user_message])
    prediction = model.predict(X_user)[0]
    
    return prediction

def get_sales_advice(question):
    """Conseils spécifiques sur la vente"""
    products = {
        "légumes": ["marchés locaux", "paniers AMAP", "vente directe à la ferme"],
        "fruits": ["cueillette à la ferme", "magasins bio", "transformation en confitures"],
        "céréales": ["coopératives agricoles", "meuneries", "circuits longs"]
    }
    
    advice = "Pour vendre vos produits, considérez: "
    for product, methods in products.items():
        if product in question.lower():
            advice += f" - {', '.join(methods)}"
            return advice
    
    return ("Conseils généraux de vente: 1) Diversifiez vos canaux de vente "
            "2) Mettez en valeur la qualité de vos produits 3) Utilisez notre "
            "plateforme pour toucher plus de clients 4) Proposez des promotions saisonnières.")

def get_irrigation_advice(question):
    """Conseils spécifiques sur l'arrosage"""
    plants = {
        "tomate": "Arrosage au pied, 2-3 fois par semaine en été",
        "salade": "Arrosage léger mais fréquent, éviter le soleil direct",
        "arbre": "Arrosage profond mais peu fréquent, privilégier le matin"
    }
    
    for plant, method in plants.items():
        if plant in question.lower():
            return f"Pour l'arrosage des {plant}s: {method}"
    
    return ("Conseils généraux d'arrosage: 1) Arrosez tôt le matin 2) Évitez "
            "de mouiller les feuilles 3) Adaptez la fréquence à la saison "
            "4) Utilisez du paillage pour conserver l'humidité")

def get_cattle_advice(question):
    """Conseils spécifiques sur l'élevage bovin"""
    if "lait" in question.lower():
        return ("Pour les vaches laitières: 1) Alimentation riche en énergie "
                "2) Eau à volonté 3) Environnement calme 4) Traite régulière "
                "5) Compléments minéraux")
    
    return ("Pour les bovins: 1) Pâturage de qualité 2) Complémentation "
            "alimentaire adaptée 3) Abreuvement adéquat 4) Suivi vétérinaire "
            "5) Conditions de vie confortables")
