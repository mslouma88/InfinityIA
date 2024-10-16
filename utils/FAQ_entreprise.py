import os

def search_in_files(question, directory):
    """Recherche la réponse à la question dans les fichiers du répertoire spécifié."""
    try:
        # Liste pour stocker les réponses trouvées
        responses = []

        # Parcourir tous les fichiers dans le répertoire
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            # Vérifier si le fichier est un fichier
            if os.path.isfile(filepath):
                # Lire le contenu du fichier selon son type
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if question.lower() in content.lower():  # Ignorer la casse
                        responses.append(f"🔍 Trouvé dans **{filename}** :\n{content[:200]}...")  # Affiche les 200 premiers caractères
        
        # Vérifier si des réponses ont été trouvées
        if responses:
            return "\n\n".join(responses)  # Renvoie toutes les réponses trouvées
        else:
            return "❌ Aucune réponse trouvée dans les fichiers spécifiés."

    except Exception as e:
        return f"⚠️ Erreur lors de la recherche : {e}"
