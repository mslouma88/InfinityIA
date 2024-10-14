import PyPDF2
import openai
import os

def analyze_cv(uploaded_file):
    try:
        # Lire le CV PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Appel à l'API OpenAI pour analyser
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Analyse ce CV et donne des suggestions d'amélioration : {text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en ressources humaines."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5,
        )
        analysis = response.choices[0].message['content'].strip()
        return analysis
    except Exception as e:
        return f"Erreur lors de l'analyse du CV : {e}"
