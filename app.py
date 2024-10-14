import streamlit as st
from PIL import Image
import datetime
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
    page_title="Synapse AI",
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
**Infinity AI** est une plateforme de collaboration créative et de productivité augmentée, assistée par une intelligence artificielle avancée. Que vous soyez un créateur, un chercheur ou une entreprise, Synapse AI est là pour vous aider à réaliser vos projets.
""")

# Onglets pour choisir ce qu'il te convient
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 Résumé de PDF", "📊 Analyse de CSV", "📚 Recommandation de Livre", "📝 Générateur de Contenu", "📄 Analyse de CV", "📄 cherchez dans un document"])


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
    st.title("Recherche dans les Documents")

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



st.sidebar.write('---')
# Ajouter un droit d'auteur
now = datetime.datetime.now()
st.sidebar.write(f"Date : {now.strftime('%Y-%m-%d')} Heure : {now.strftime('%H:%M')}")
st.sidebar.write(f"© {now.year} Salam & Nesrine")