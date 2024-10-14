import openai
import os

def generate_content(subject):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Génère un contenu détaillé sur le sujet suivant : {subject}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un générateur de contenu créatif intelligent."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7,
        )
        content = response.choices[0].message['content'].strip()
        return content
    except Exception as e:
        return f"Erreur lors de la génération de contenu : {e}"
