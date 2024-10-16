import os
import openai
from typing import List, Dict
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

class RechercheDocumentaireWeb:
    def __init__(self):
        # Récupérer la clé API depuis les variables d'environnement
        self.api_key_openai = os.getenv("OPENAI_API_KEY")
        self.api_key_search = os.getenv("SEARCH_API_KEY")  # Si vous avez aussi une clé pour un moteur de recherche
        openai.api_key = self.api_key_openai  # Initialiser l'API OpenAI

    def rechercher_sur_internet(self, requete: str) -> List[Dict[str, str]]:
        # Exemple avec une API de moteur de recherche (comme SerpAPI)
        url = "https://serpapi.com/search"
        params = {
            "q": requete,
            "api_key": self.api_key_search,  # Clé pour le moteur de recherche
            "num": 10  # Limiter à 10 résultats pour cet exemple
        }
        response = requests.get(url, params=params)
        resultats = response.json().get('organic_results', [])

        documents_trouves = []
        for resultat in resultats:
            titre = resultat.get('title', 'Titre non disponible')
            lien = resultat.get('link', 'Lien non disponible')
            extrait = resultat.get('snippet', 'Aucun extrait disponible')

            # Utiliser l'API OpenAI pour évaluer la pertinence
            reponse = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant de recherche documentaire."},
                    {"role": "user", "content": f"Ce document est-il pertinent pour la requête '{requete}'? Répondez par Oui ou Non, suivi d'une explication : {extrait}"}
                ]
            )

            # Vérifier si la réponse contient "oui"
            if "oui" in reponse.choices[0].message['content'].lower():
                documents_trouves.append({
                    "titre": titre,
                    "lien": lien,
                    "extrait": extrait
                })

        return documents_trouves
