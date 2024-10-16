import streamlit as st
from PIL import Image
import datetime
from gtts import gTTS
import requests, openai, random ,io ,pygame

from utils.pdf_summary import summarize_pdf
from utils.csv_analysis import analyze_csv
from utils.book_recommendation import recommend_books
from utils.content_generator import generate_content
from utils.cv_analysis import analyze_cv
#from utils.document_search import search_documents

from dotenv import load_dotenv
# Chargez les variables d'environnement à partir du fichier .env
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Infinity AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
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

# Define the themes
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
    "Blue":  {
        "background-color": "#000000",
        "color": "#00FFFF",
        "button-background-color": "#00FFFF",
        "button-color": "#000000",
        "button-box-shadow": "0 0 10px #00FFFF",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#00FFFF",
        "sidebar-box-shadow": "0 0 10px #00FFFF",
    },
    "Gaming": {
        "background-color": "#1F1F1F",
        "color": "#FFD700",
        "button-background-color": "#FFD700",
        "button-color": "#1F1F1F",
        "button-box-shadow": "0 0 10px #FFD700",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#FFD700",
        "sidebar-box-shadow": "0 0 10px #FFD700",
    },
    "Neon": {
        "background-color": "#1A1A1D",
        "color": "#00FF00",
        "button-background-color": "#00FF00",
        "button-color": "#1A1A1D",
        "button-box-shadow": "0 0 20px #00FF00",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#00FF00",
        "sidebar-box-shadow": "0 0 20px #00FF00",
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
logo = Image.open("assets/INFINITYAI.png")
#banner = Image.open("assets/Banniere.gif")

# Affichage du logo et de la bannière
st.sidebar.image(logo, width=300)
#st.image(banner, use_column_width=True)

# Add a theme selection dropdown menu to the sidebar
selected_theme = st.sidebar.selectbox("🎨 Choisissez un thème", list(themes.keys()), index=0)
update_theme(selected_theme)

st.title("Bienvenue sur Infinity AI")

st.markdown("""
**Infinity AI** est une plateforme alimentée par une intelligence artificielle avancée, conçue pour booster votre créativité et votre productivité. Elle offre une large gamme de fonctionnalités pour accompagner les créateurs, chercheurs et entreprises dans leurs projets :
""")
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Onglets pour choisir ce qu'il te convient
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["📝 Résumé de PDF", "📊 Analyse de CSV", "📚 Recommandation de Livre", "📝 Générateur de Contenu", "📄 Analyse de CV", "📄 cherchez dans un document", "⚕️ Recherche Médicale", "💼 FAQ Entreprise"])


# Fonctionnalité : Résumé de PDF
with tab1:
    st.header("Résumé de PDF")
    uploaded_file = st.file_uploader("Téléchargez votre fichier PDF", type="pdf")
    if uploaded_file is not None:
        summary = summarize_pdf(uploaded_file)
        st.subheader("Résumé :")
        st.write(summary)


# Fonctionnalité : Analyse de CSV
with tab2:
    st.header("Analyse de Fichier CSV")
    uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type="csv")
    if uploaded_file is not None:
        analysis = analyze_csv(uploaded_file)
        if "error" in analysis:
            st.error(analysis["error"])
        else:
            st.subheader("Résumé statistique :")
            st.dataframe(analysis['data'])
       
            st.subheader("Analyse :")
            st.write(analysis['ai_analysis'])


# Fonctionnalité : Recommandation de Livre
with tab3:
    st.header("Recommandation de Livre")
    genre = st.text_input("Entrez votre genre préféré :", "Science-fiction")
    if st.button("Recommander"):
        recommendations = recommend_books(genre)
        st.subheader("Livres Recommandés :")
        for book in recommendations:
            st.write(f"- {book}")


# Fonctionnalité : Générateur de Contenu
with tab4:
    st.header("Générateur de Contenu")
    subject = st.text_input("Entrez le sujet :", "Intelligence Artificielle")
    if st.button("Générer"):
        content = generate_content(subject)
        st.subheader("Contenu Généré :")
        st.write(content)


# Fonctionnalité : Analyse de CV
with tab5:
    st.header("Analyse de CV")
    uploaded_file = st.file_uploader("Téléchargez votre CV (PDF)", type="pdf")
    if uploaded_file is not None:
        analysis = analyze_cv(uploaded_file)
        st.subheader("Analyse du CV :")
        st.write(analysis)

with tab6:
    st.header("Recherche dans les Documents")

    uploaded_files = st.file_uploader("Téléchargez vos documents (PDF, TXT)", type=["pdf", "txt"], accept_multiple_files=True)

    if uploaded_files:
        user_question = st.text_input("Posez votre question sur les documents téléchargés :")
        if st.button("Rechercher"):
            if user_question:
                with st.spinner("Recherche en cours..."):
                    answer = search_documents(uploaded_files, user_question)
                st.subheader("Réponse :")
                st.write(answer)
            else:
                st.warning("Veuillez entrer une question.")
    else:
        st.info("Veuillez télécharger des documents pour commencer.")

with tab7:

    # Moteur de Recherche Médicale
    st.header("Moteur de Recherche Médicale")
    question_med = st.text_input("Posez votre question médicale :")
    if st.button("Rechercher Médicale"):
        # Exemple d'utilisation de l'API PubMed
        pubmed_url = f"https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=citation&size=5&term={question_med}"
        response = requests.get(pubmed_url)
        articles = response.json()
        context_med = " ".join([article['title'] + " " + article['abstract'] for article in articles.get('results', [])])
        prompt_med = f"Répondez à la question suivante en utilisant les informations suivantes : {context_med}\nQuestion : {question_med}"
        answer_med = generate_response(prompt_med)
        st.write(answer_med)

# Chatbot pour FAQ d’Entreprise
with tab8:
    tabs = st.tabs([
    "🔍 Recherche Documentaire",
    "💼 FAQ Entreprise"])
    with tabs[0]:
        st.header("Chatbot pour FAQ d'Entreprise")
    with tabs[1]:
        # Section de l'assistant IA
        st.header("Assistant IA")

        user_input = st.text_input("Posez une question ou décrivez votre projet :", "")

        if st.button("Générer une réponse"):
            if user_input:
                openai.api_key = os.getenv("OPENAI_API_KEY")
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Vous êtes un assistant utile, inteligent, et respectueux qui  aide les utilisateurs à résoudre leurs problèmes et à atteindre leurs objectifs."},

                            {"role": "user", "content": user_input},
                        ],
                        max_tokens=2000,
                        n=1,
                        stop=None,
                        temperature=0.7,
                    )
                    answer = response.choices[0].message['content'].strip()
                    st.write(answer)
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")
            else:
                st.write("Veuillez entrer une question ou une description.")


# Initialisation de pygame pour la lecture audio
pygame.mixer.init()
def speak_text(text):
    # Créer un objet gTTS
    tts = gTTS(text=text, lang='fr')
    
    # Créer un tampon en mémoire
    fp = io.BytesIO()
    
    # Sauvegarder l'audio dans le tampon en mémoire
    tts.write_to_fp(fp)
    
    # Rembobiner le tampon au début
    fp.seek(0)
    
    try:
        # Charger l'audio depuis le tampon en mémoire
        pygame.mixer.music.load(fp)
        
        # Jouer l'audio
        pygame.mixer.music.play()
        
        # Attendre que la lecture soit terminée
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    except Exception as e:
        st.error(f"Erreur lors de la lecture audio : {e}")
    
    finally:
        # Nettoyer le tampon en mémoire
        fp.close()


# Easter egg
if st.sidebar.button("🎁 Surprise !"):
    jokes = [
        "Pourquoi les robots ne prennent-ils jamais de vacances ? Parce qu'ils ont déjà trop de vis !",
        "Comment s'appelle un robot qui fait toujours la même chose ? Un automate.",
        "Que dit un robot quand il tombe en panne ? 'J'ai un bug-out-bag !'",
    ]
    joke = random.choice(jokes)
    st.sidebar.write(joke)
    speak_text(joke)


st.sidebar.write('---')
# Ajouter un droit d'auteur
now = datetime.datetime.now()
st.sidebar.write(f"Date : {now.strftime('%Y-%m-%d')} Heure : {now.strftime('%H:%M')}")
st.sidebar.write(f"© {now.year} Salam & Nesrine")