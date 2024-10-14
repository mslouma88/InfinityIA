import openai
import os


def recommend_books(genre):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Recommande-moi 5 livres populaires dans le genre {genre}."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en littérature mais aussi dans tout domaine."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7,
        )
        recommendations = response.choices[0].message['content'].strip()
        # Split the recommendations into a list
        books = [book.strip() for book in recommendations.split('\n') if book]
        return books
    except Exception as e:
        return [f"Erreur lors de la recommandation de livres : {e}"]
