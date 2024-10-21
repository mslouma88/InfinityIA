import os
import openai
from typing import List
from pypdf import PdfReader
import tiktoken


def load_documents(uploaded_files: List[object]) -> str:
    """
    Charge les documents téléchargés (PDF et TXT) et retourne leur contenu sous forme de texte.
    """
    all_text = ""
    for file in uploaded_files:
        try:
            if file.type == "application/pdf":
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    all_text += page.extract_text() + "\n"
            elif file.type == "text/plain":
                all_text += file.getvalue().decode("utf-8") + "\n"
            else:
                print(f"Type de fichier non supporté : {file.type}")
        except Exception as e:
            print(f"Erreur lors du chargement du fichier {file.name} : {e}")
    return all_text

def truncate_text(text: str, max_tokens: int = 3000) -> str:
    """
    Tronque le texte pour qu'il ne dépasse pas le nombre maximum de tokens.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        return encoding.decode(tokens[:max_tokens])
    return text

def search_documents(uploaded_files: List[object], question: str) -> str:
    """
    Recherche dans les documents téléchargés et retourne une réponse basée sur la question posée.
    """
    try:
        # Charger les documents
        document_text = load_documents(uploaded_files)
        if not document_text:
            return "Aucun document valide téléchargé."

        # Tronquer le texte si nécessaire
        truncated_text = truncate_text(document_text)

        # Préparer le prompt pour GPT
        prompt = f"""Contexte: {truncated_text}

Question: {question}

Réponse :"""

        # Appeler l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant utile qui répond aux questions basées sur le contexte fourni."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extraire et retourner la réponse
        answer = response.choices[0].message['content'].strip()
        return f"Réponse : {answer}"

    except Exception as e:
        return f"Une erreur est survenue lors de la recherche dans les documents : {e}"