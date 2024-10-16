import requests
import openai
import os

def search_medical_articles(question_med):
    """Recherche des articles médicaux à partir de PubMed en fonction de la question médicale de l'utilisateur."""
    try:
        # Utiliser l'API de recherche de PubMed
        pubmed_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={question_med}&retmode=xml&retmax=5"
        
        # Effectuer la requête à l'API PubMed
        response = requests.get(pubmed_url)
        response.raise_for_status()
        
        # Extraire les IDs des articles trouvés
        articles_data = response.text
        
        # Récupérer les détails de chaque article en utilisant l'API de PubMed
        ids = [line.split("<Id>")[1].split("</Id>")[0] for line in articles_data.splitlines() if "<Id>" in line]
        if not ids:
            return "📄 Aucun article pertinent trouvé dans PubMed pour cette recherche."
        
        # Construire la requête pour obtenir les détails des articles
        id_string = ",".join(ids)
        details_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id_string}&retmode=xml"
        
        details_response = requests.get(details_url)
        details_response.raise_for_status()

        # Extraire les titres et résumés des articles
        articles_details = details_response.text
        context_med = []
        for line in articles_details.splitlines():
            if "<ArticleTitle>" in line:
                title = line.split("<ArticleTitle>")[1].split("</ArticleTitle>")[0]
                context_med.append(title)
            if "<AbstractText>" in line:
                abstract = line.split("<AbstractText>")[1].split("</AbstractText>")[0]
                context_med.append(abstract)

        context_med_str = " ".join(context_med)

        if not context_med_str.strip():
            return "📄 Aucun article pertinent trouvé dans PubMed pour cette recherche."

        return context_med_str

    except Exception as e:
        return f"❌ Erreur lors de la recherche sur PubMed : {e}"

def generate_medical_response(context_med, question_med):
    """Génère une réponse médicale en utilisant le contexte des articles PubMed et la question de l'utilisateur."""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt_med = f"Voici des articles médicaux : {context_med}. Répondez à la question suivante : {question_med}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Tu es un expert médical qui répond aux questions en se basant sur des articles scientifiques."},
                      {"role": "user", "content": prompt_med}],
            max_tokens=1500,
            temperature=0.5,
        )
        answer_med = response.choices[0].message['content'].strip()
        return answer_med

    except Exception as e:
        return f"❌ Erreur lors de la génération de la réponse : {e}"
