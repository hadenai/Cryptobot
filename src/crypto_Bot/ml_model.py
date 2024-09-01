from crypto_Bot.models import Klines
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import pickle
import os

def get_crypto_data(crypto: str, start_timestamp: int, end_timestamp: int):
    conn = sqlite3.connect('crypto_data.db')  # Connexion à la base de données SQLite
    query = f"""
        SELECT open_time, open_price, high_price, low_price, close_price, volume_assets
        FROM {crypto}  # Sélectionne toutes les colonnes nécessaires de la table spécifiée par la variable 'crypto'
        WHERE open_time >= {start_timestamp} AND open_time <= {end_timestamp}  # Filtre les données par intervalle de temps
        ORDER BY open_time ASC  # Trie les données par ordre croissant de temps
    """
    data = pd.read_sql_query(query, conn)  # Exécute la requête et lit les données dans un DataFrame Pandas
    conn.close()  # Ferme la connexion à la base de données
    return data

# Fonction pour créer des bougies de durée variable
def create_candles(data, interval):
    candles = []  # Liste pour stocker les bougies
    for i in range(0, len(data), interval):  # Itère sur les données par tranche de 'interval' minutes
        chunk = data.iloc[i:i+interval]  # Sélectionne une tranche de données de taille 'interval'
        if len(chunk) < interval:  # Si la tranche est plus petite que l'intervalle, passe à la tranche suivante
            continue
        # Agrégation des données pour créer une bougie
        open_time = chunk.iloc[0]['open_time']
        open_price = chunk.iloc[0]['open_price']
        high_price = chunk['high_price'].max()
        low_price = chunk['low_price'].min()
        close_price = chunk.iloc[-1]['close_price']
        volume_assets = chunk['volume_assets'].sum()
        # Ajoute la bougie à la liste
        candles.append((open_time, open_price, high_price, low_price, close_price, volume_assets))
    # Convertit la liste de bougies en DataFrame Pandas
    return pd.DataFrame(candles, columns=['open_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume_assets'])

# Fonction pour entraîner et prédire avec les modèles
def train_and_predict_model(model_type, data):
    # Définition de la target comme étant 1 si le prix de clôture suivant est supérieur au prix de clôture actuel, sinon 0
    data['target'] = data['close_price'].shift(-1) > data['close_price']
    data.dropna(inplace=True)  # Supprime les lignes avec des valeurs NaN, qui apparaissent après le décalage

    # Sélection des features (caractéristiques) et de la target (variable à prédire)
    X = data[['open_price', 'high_price', 'low_price', 'close_price', 'volume_assets']]
    y = data['target'].astype(int)  # Conversion de la target en entier (0 ou 1)

    # Définir le nom de fichier pour sauvegarder le modèle
    model_filename = f"{model_type}_model.pkl"

    # Vérifier si un modèle sauvegardé existe
    if os.path.exists(model_filename):
        with open(model_filename, 'rb') as file:
            model = pickle.load(file)
        print(f"Loaded {model_type} model from {model_filename}")
    else:
        # Sélection du modèle en fonction du type spécifié
        if model_type == 'linear':
            model = LinearRegression()
        elif model_type == 'logistic':
            model = LogisticRegression()
        elif model_type == 'decision_tree':
            model = DecisionTreeClassifier()
        elif model_type == 'random_forest':
            model = RandomForestClassifier()
        else:
            raise ValueError("Invalid model type specified")  # Erreur si le type de modèle est invalide

        # Entraînement du modèle
        model.fit(X, y)

        # Sauvegarder le modèle entraîné
        with open(model_filename, 'wb') as file:
            pickle.dump(model, file)
        print(f"Saved {model_type} model to {model_filename}")

    # Prédire la target pour la dernière ligne de données
    prediction = model.predict([X.iloc[-1]])[0]
    decision = "Buy" if prediction == 1 else "Sell"

    return decision  # Retourne la décision d'achat ou de vente
# 
def result_ml(model_choice: str, interval_min: int, candlestick_count: int):
    crypto = 'BTC'
    end_time = datetime.now()  # Temps actuel
    start_time = end_time - timedelta(minutes=interval*num_candles)  # Temps de début basé sur le nombre de bougies et l'intervalle

    # Conversion des temps en timestamps en millisecondes
    end_timestamp = int(end_time.timestamp() * 1000)
    start_timestamp = int(start_time.timestamp() * 1000)

    # Récupération des données de la base de données
    data = get_crypto_data(crypto, start_timestamp, end_timestamp)
    # Création des bougies de la durée spécifiée
    candles = create_candles(data, interval)

    # Entraînement et prédiction avec le modèle spécifié
    decision = train_and_predict_model(model_type, candles)

    # Retourne la décision d'achat ou de vente
    return {"decision": decision}
