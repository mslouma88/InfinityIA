import openai
import os

# Dictionnaire d'emojis par genre
emojis_par_genre = {
    "science-fiction": "🚀",
    "fantasy": "🧙‍♂️",
    "romance": "❤️",
    "horreur": "👻",
    "thriller": "🔪",
    "historique": "🏺",
    "aventure": "🌍",
    "poésie": "📝",
}

def get_genre_emoji(genre):
    """Retourne un emoji en fonction du genre."""
    return emojis_par_genre.get(genre.lower(), "📚")

def recommend_books(genre):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        emoji = get_genre_emoji(genre)
        prompt = f"Recommande-moi 5 livres populaires dans le genre {genre}."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en littérature mais aussi dans tout domaine."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500, 
            temperature=0.7,
        )
        recommendations = response.choices[0].message['content'].strip()
        # Séparer les recommandations en une liste
        books = [f"{emoji} {book.strip()}" for book in recommendations.split('\n') if book]
        return books
    except Exception as e:
        return [f"❌ Erreur lors de la recommandation de livres : {e}"]
