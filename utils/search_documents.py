from pypdf import PdfReader
import os
import openai

def extract_text_from_pdf(pdf_file):
    """Extrait le texte d'un fichier PDF."""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"❌ Erreur lors de l'extraction du PDF : {e}"

def extract_text_from_txt(txt_file):
    """Extrait le texte d'un fichier TXT."""
    try:
        return txt_file.read().decode('utf-8')
    except Exception as e:
        return f"❌ Erreur lors de l'extraction du fichier TXT : {e}"

def search_documents(uploaded_files, user_question):
    """Recherche la réponse à la question de l'utilisateur dans les documents téléchargés."""
    all_text = ""
    for file in uploaded_files:
        if file.type == "application/pdf":
            all_text += extract_text_from_pdf(file)
        elif file.type == "text/plain":
            all_text += extract_text_from_txt(file)

    if not all_text.strip():
        return "📄 Aucun texte n'a été extrait des documents fournis."

    # Appel à l'API OpenAI pour répondre à la question en fonction du texte extrait
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Voici des documents : {all_text}. Répondez à la question suivante : {user_question}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant intelligent qui répond aux questions à partir de documents fournis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return f"❌ Erreur lors de la recherche dans les documents : {e}"
