import PyPDF2
import openai
import os

def summarize_pdf(uploaded_file):
    try:
        # Lire le PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Vérifier si le texte est vide
        if not text.strip():
            return "📄 Le PDF semble être vide ou non lisible."

        # Appel à l'API OpenAI pour résumer
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui résume des documents PDF."},
                {"role": "user", "content": f"Résumé le contenu suivant : {text}"}
            ],
            max_tokens=1500,  # Limité pour avoir des résumés plus rapides
            temperature=0.5,
        )
        summary = response.choices[0].message['content'].strip()
        return summary
    except Exception as e:
        return f"❌ Erreur lors du résumé du PDF : {e}"
