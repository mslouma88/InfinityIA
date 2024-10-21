import streamlit as st
from PIL import Image
import datetime
from gtts import gTTS
import openai, random , os
from textblob import TextBlob

from utils.pdf_summary import summarize_pdf
from utils.csv_analysis import analyze_csv
from utils.book_recommendation import recommend_books
from utils.content_generator import generate_content
from utils.cv_analysis import analyze_cv
from utils.document_search import search_documents
from utils.Recherche_Documentaire import RechercheDocumentaireWeb
from utils.search_documents import search_documents
from utils.medical_search import search_medical_articles, generate_medical_response

from dotenv import load_dotenv
# Chargez les variables d'environnement à partir du fichier .env
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Bienvenue Infinity AI",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style pour le titre animé :)
st.markdown(
    """
    <style>
    .title {
        font-size: 3em;
        color: #ef9900;  
        text-align: left;
        animation: fadeIn 5s;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    </style>
    <h1 class="title">Bienvenue sur Infinity AI ♾️</h1>
    """,
    unsafe_allow_html=True
)


# Définir le style CSS personnalisé
custom_css = """
<style>
    [data-testid=stSidebar] {
        background-color: #0D1117;
    }
</style>
"""

# Appliquer le style CSS personnalisé
st.markdown(custom_css, unsafe_allow_html=True)

# Define the themes #A6A957
themes = {
    "Dark Mode": {
        "background-color": "#0D1117",   
        "color": "#FFFFFF",
        "button-background-color": "#FFFFFF",
        "button-color": "#1E1E1E",
        "button-box-shadow": "0 0 10px #FFFFFF",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#FFFFFF",
        "sidebar-box-shadow": "0 0 10px #FFFFFF",
    },
    "Rose":  {
        "background-color": "#0D1117",
        "color": "#FFFFFF",
        "button-background-color": "#cf1e4e",
        "button-color": "#000000",
        "button-box-shadow": "0 0 10px #cf1e4e",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#cf1e4e",
        "sidebar-box-shadow": "0 0 10px #cf1e4e",
    },
    "Gaming": {
        "background-color": "#0D1117",
        "color": "#FFFFFF",
        "button-background-color": "#ef9900",
        "button-color": "#1F1F1F",
        "button-box-shadow": "0 0 10px #ef9900",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#FFD700",
        "sidebar-box-shadow": "0 0 10px #FFD700",
    },
    "Neon": {
        "background-color": "#0D1117",  
        "color": "#FFFFFF",
        "button-background-color": "#00c599",
        "button-color": "#1A1A1D",
        "button-box-shadow": "0 0 20px #00c599",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#00c599",
        "sidebar-box-shadow": "0 0 20px #00c599",
    },
}


# Set the initial theme #0D1117
theme = "Dark Mode"

# Define a function to update the theme
def update_theme(theme):
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {themes[theme]['background-color']};
            color: {themes[theme]['color']};
            font-family: 'Courier New', Courier, monospace;
        }}
        .stButton>button {{
            background-color: {themes[theme]['button-background-color']};
            color: {themes[theme]['button-color']};
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: {themes[theme]['button-box-shadow']};
        }}
        .stButton>button:hover {{
            background-color: {themes[theme]['button-color']};
            color: {themes[theme]['button-background-color']};
            border: 2px solid {themes[theme]['button-background-color']};
            box-shadow: 0 0 20px {themes[theme]['button-background-color']};
        }}
        .stSidebar {{
            background-color: {themes[theme]['sidebar-background-color']};
            color: {themes[theme]['sidebar-color']};
            box-shadow: {themes[theme]['sidebar-box-shadow']};
        }}
        </style>
    """, unsafe_allow_html=True)

# Chargement des images
logo = Image.open("assets/logo.png")
#banner = Image.open("assets/Banniere.gif")

# Affichage du logo et de la bannière
st.sidebar.image(logo, width=300)
#st.image(banner, use_column_width=True)

# Add a theme selection dropdown menu to the sidebar
selected_theme = st.sidebar.selectbox("🎨 Choisissez un thème", list(themes.keys()), index=0)
update_theme(selected_theme)

#st.title("Bienvenue sur Infinity AI")

st.markdown("""
**Infinity AI** est une plateforme alimentée par une intelligence artificielle avancée, conçue pour booster votre créativité et votre productivité. Elle offre une large gamme de fonctionnalités pour accompagner les étudiants, les créateurs, chercheurs et les entreprises dans leurs projets :
""")
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Initialiser le contexte de la conversation
if 'context' not in st.session_state:
    st.session_state.context = []

# Zone de conversation
conversation = st.empty()

def update_conversation():
    conversation.text_area("📜 **Historique de la conversation**", 
                           value="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.context]),
                           height=300)

# Fonction pour analyser le sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.1:
        return "positif"
    elif sentiment < -0.1:
        return "négatif"
    else:
        return "neutre"
    
# Fonction pour interroger l'API OpenAI avec contexte
def ask_openai(prompt, context):
    messages = [{"role": "system", "content": "Vous êtes un assistant vocal futuriste, intelligent et serviable."}]
    messages.extend(context)
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
# Fonction pour générer une réponse de l'assistant IA
def generate_ai_response(user_input):
    """Génère une réponse de l'assistant IA à partir de l'entrée de l'utilisateur."""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant utile, intelligent et respectueux qui aide les utilisateurs à résoudre leurs problèmes et à atteindre leurs objectifs."},
                {"role": "user", "content": user_input},
            ],
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return f"⚠️ Une erreur est survenue : {e}"

# Onglets pour choisir ce qu'il te convient
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📝 Résumé de PDF", "📊 Analyse de CSV", "📚 Recommandation de Livre", "📝 Générateur de Contenu", "📄 Analyse de CV", "🔍 cherchez dans un document",  "⏩ Suivant"])


# Fonctionnalité : Résumé de PDF
with tab1:
    st.header("📝 Résumé de PDF")
    uploaded_file = st.file_uploader("📂 Téléchargez votre fichier PDF", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("⏳ Résumé en cours..."):
            summary = summarize_pdf(uploaded_file)
        
        if "Erreur" in summary:
            st.error(summary)
        else:
            st.subheader("📄 Résumé :")
            st.write(summary)


# Fonctionnalité : Analyse de CSV
with tab2:
    st.header("📊 Analyse de Fichier CSV")
    uploaded_file = st.file_uploader("📂 Téléchargez votre fichier CSV", type="csv")
    
    if uploaded_file is not None:
        with st.spinner("⏳ Analyse en cours..."):
            analysis = analyze_csv(uploaded_file)
        
        if "error" in analysis:
            st.error(analysis["error"])
        else:
            st.subheader("📋 Résumé statistique :")
            st.dataframe(analysis['data'])
       
            st.subheader("💡 Analyse IA :")
            st.write(analysis['ai_analysis'])

# Fonctionnalité : Recommandation de Livre
with tab3:
    st.header("📚 Recommandation de Livre")
    genre = st.text_input("Entrez votre genre préféré :", "Science-fiction")
    
    if st.button("Recommander"):
        with st.spinner("🔍 Recherche de recommandations..."):
            recommendations = recommend_books(genre)
        st.subheader("📖 Livres Recommandés :")
        for book in recommendations:
            st.write(f"- {book}")


# Fonctionnalité : Générateur de Contenu
with tab4:
    st.header("📝 Générateur de Contenu")
    
    subject = st.text_input("💡 Entrez le sujet :", "Intelligence Artificielle")
    
    if st.button("🚀 Générer le Contenu"):
        with st.spinner("⏳ Génération du contenu en cours..."):
            content = generate_content(subject)
        
        if "Erreur" in content:
            st.error(content)
        else:
            st.subheader("📄 Contenu Généré :")
            st.write(content)

# Fonctionnalité : Analyse de CV
with tab5:
    st.header("🔍 Analyse de CV")
    
    uploaded_file = st.file_uploader("📂 Téléchargez votre CV (PDF)", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("⏳ Analyse du CV en cours..."):
            analysis = analyze_cv(uploaded_file)
        
        if "Erreur" in analysis:
            st.error(analysis)
        else:
            st.subheader("📝 Résultats de l'Analyse du CV :")
            st.write(analysis)

# Fonctionnalité : Recherche dans les Documents
with tab6:
    st.header("🔍 Recherche dans les Documents")

    uploaded_files = st.file_uploader("📂 Téléchargez vos documents (PDF, TXT)", type=["pdf", "txt"], accept_multiple_files=True)

    if uploaded_files:
        user_question = st.text_input("💬 Posez votre question sur les documents téléchargés :")

        if st.button("🔎 Rechercher"):
            if user_question:
                with st.spinner("⏳ Recherche en cours..."):
                    answer = search_documents(uploaded_files, user_question)
                
                if "Erreur" in answer:
                    st.error(answer)
                else:
                    st.subheader("📄 Réponse :")
                    st.write(answer)
            else:
                st.warning("⚠️ Veuillez entrer une question.")
    else:
        st.info("ℹ️ Veuillez télécharger des documents pour commencer.")


# Chatbot pour FAQ d’Entreprise
with tab7:
    tabs = st.tabs([
    "⚕️ Recherche Médicale",
    "🔍 Recherche Documentaire",
    "🤖 IA Entreprise",
    "💬 Chat Écrit"])

    # Fonctionnalité : Moteur de Recherche Médicale
    with tabs[0]: 
        st.header("🩺 Moteur de Recherche Médicale")

        question_med = st.text_input("💬 Posez votre question médicale :")

        if st.button("🔎 Rechercher Médicale"):
            if question_med:
                with st.spinner("⏳ Recherche en cours dans les bases de données médicales..."):
                    context_med = search_medical_articles(question_med)
                    
                if "Erreur" in context_med:
                    st.error(context_med)
                else:
                    with st.spinner("⏳ Génération de la réponse médicale..."):
                        answer_med = generate_medical_response(context_med, question_med)

                    if "Erreur" in answer_med:
                        st.error(answer_med)
                    else:
                        st.subheader("📄 Réponse :")
                        st.write(answer_med)
            else:
                st.warning("⚠️ Veuillez entrer une question médicale.")

    # Créer un onglet pour la recherche web
    with tabs[1]:
        st.header("🔍 Recherche Documentaire Web")

        # Champ de recherche
        requete = st.text_input("Entrez votre requête de recherche :")

        # Bouton de recherche
        if st.button("Rechercher"):
            if not requete:
                st.error("Veuillez entrer une requête de recherche.")
            else:
                with st.spinner("Recherche en cours sur Internet..."):
                    # Créer une instance de la classe RechercheDocumentaireWeb
                    recherche = RechercheDocumentaireWeb()
                    resultats = recherche.rechercher_sur_internet(requete)

                    if not resultats:
                        st.info("🔍 Aucun document pertinent trouvé.")
                    else:
                        st.success(f"🎉 {len(resultats)} document(s) pertinent(s) trouvé(s) sur Internet!")
                        for i, doc in enumerate(resultats, 1):
                            with st.expander(f"📄 {doc['titre']}"):
                                st.write(f"🔗 Lien : {doc['lien']}")
                                st.write(f"📝 Extrait : {doc['extrait']}")

        # Section de l'assistant IA
    with tabs[2]:
        st.header("🤖 Assistant IA")

        user_input = st.text_input("💬 Posez une question ou décrivez votre projet :", "")

        if st.button("✨ Générer une réponse"):
            if user_input:
                with st.spinner("⏳ Génération de la réponse..."):
                    answer = generate_ai_response(user_input)
                    st.subheader("📄 Réponse :")
                    st.write(answer)
            else:
                st.warning("⚠️ Veuillez entrer une question ou une description.")
    
    # Section de l'assistant IA
    with tabs[3]:
        # Zone de saisie de texte
        user_input = st.text_input("📝 Écrivez votre message ici")

        # Si l'utilisateur veut envoyer le message
        if st.button("🚀 Envoyer"):
            if user_input:
                # Analyser le sentiment
                sentiment = analyze_sentiment(user_input)
                st.write(f"**Sentiment détecté** : {sentiment}")

                # Interroger ChatGPT
                response = ask_openai(user_input, st.session_state.context)
                st.write(f"**🤖 Agent** : {response}")

                # Ajouter au contexte
                st.session_state.context.append({"role": "🙋 Moi", "content": user_input})
                st.session_state.context.append({"role": "👾 Agent Infinity", "content": response})

                # Mettre à jour la zone de conversation
                update_conversation()
            else:
                st.warning("⚠️ Veuillez écrire un message avant d'envoyer.")


            # Bouton pour effacer l'historique
            if st.button("🗑️ Effacer l'historique"):
                st.session_state.context = []
                update_conversation()
                st.success("Historique effacé !")


# Easter egg
if st.sidebar.button("🎁 Surprise !"):
    jokes = [
        "Pourquoi les robots ne prennent-ils jamais de vacances ? Parce qu'ils ont déjà trop de vis ! 🤖🔧",
        "Comment s'appelle un robot qui fait toujours la même chose ? Un automate. 🛠️",
        "Que dit un robot quand il tombe en panne ? 'J'ai un bug-out-bag !' 🐞",
        "Pourquoi le robot a-t-il traversé la route ? Pour aller à l'autre circuit ! 🛣️",
        "Pourquoi les ordinateurs n'aiment-ils pas la chaleur ? Parce qu'ils ont peur de surchauffer ! ☀️💻",
        "Quel est le plat préféré des robots ? Les algorithmes à la sauce binaire ! 🍽️",
        "Pourquoi les robots adorent-ils les jeux de société ? Parce qu'ils aiment les défis sans fil ! 🎲",
        "Que dit un robot qui veut sortir ? 'J'ai besoin d'une mise à jour d'ambiance !' 🎉"
    ]
    
    joke = random.choice(jokes)
    st.sidebar.write(joke)
#    speak_text(joke)


st.sidebar.write('---')
# Ajouter un droit d'auteur
now = datetime.datetime.now()
st.sidebar.write(f"Date : {now.strftime('%Y-%m-%d')} Heure : {now.strftime('%H:%M')}")
st.sidebar.write(f"© {now.year} Salam & Nesrine")