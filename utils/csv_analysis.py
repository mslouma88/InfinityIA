import pandas as pd
import openai
import os


def generate_ai_analysis(df_info):
    prompt = f"""En tant qu'analyste de données, examinez les informations suivantes sur un ensemble de données et fournissez une analyse approfondie :

{df_info}

Veuillez inclure :
1. Un résumé des principales caractéristiques du dataset
2. Des observations sur la distribution des données
3. Des corrélations potentielles entre les variables
4. Des suggestions pour une analyse plus approfondie
5. Des recommandations pour améliorer la qualité des données si nécessaire

Limitez votre réponse à environ 300 mots."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vous êtes un analyste de données expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

def analyze_csv(uploaded_file):
    try:
        # Lire le CSV
        df = pd.read_csv(uploaded_file)

        # Description des données
        description = df.describe()
        
        # Informations générales sur le dataset
        df_info = f"""
        Nombre de lignes : {df.shape[0]}
        Nombre de colonnes : {df.shape[1]}
        Colonnes : {', '.join(df.columns)}
        Types de données :
        {df.dtypes.to_string()}
        
        Résumé statistique :
        {description.to_string()}
        
        Valeurs manquantes :
        {df.isnull().sum().to_string()}
        """

        # Générer l'analyse AI
        ai_analysis = generate_ai_analysis(df_info)


        return {
            "data": description,
            "ai_analysis": ai_analysis
        }
    except Exception as e:
        return {"error": f"❌ Erreur lors de l'analyse du CSV : {e}"}
