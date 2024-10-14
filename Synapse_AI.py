import streamlit as st
from PIL import Image
import openai
import os
from dotenv import load_dotenv
import datetime
import speech_recognition as sr
import random
from gtts import gTTS
from textblob import TextBlob
import io

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

# Chargement des images
logo = Image.open("assets/Logo_Synapse_AI.png")
#banner = Image.open("assets/banner.png")

# Affichage du logo et de la bannière
st.sidebar.image(logo, width=300)
#st.image(banner, use_column_width=True)


# Fonction de reconnaissance vocale améliorée
def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        st.write("🎧 **Écoute active...**")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            st.error("Aucune parole détectée. Veuillez réessayer.")
            return None

    try:
        text = recognizer.recognize_google(audio, language='fr-FR')
        return text
    except sr.UnknownValueError:
        return "Je n'ai pas compris. Pouvez-vous répéter ?"
    except sr.RequestError:
        return "Erreur de connexion au service de reconnaissance vocale."

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

# Fonction pour la synthèse vocale avec gTTS
def speak_text(text):
    # Créer un objet gTTS
    tts = gTTS(text=text, lang='fr')
    
    # Créer un tampon en mémoire
    fp = io.BytesIO()
    
    # Sauvegarder l'audio dans le tampon en mémoire
    tts.write_to_fp(fp)
    
    # Rembobiner le tampon au début
    fp.seek(0)
    
    return fp

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



# Define the themes
themes = {
    "Dark Mode": {
        "background-color": "#121212",
        "color": "#FFFFFF",
        "button-background-color": "#FFFFFF",
        "button-color": "#121212",
        "button-box-shadow": "0 0 10px #FFFFFF",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#FFFFFF",
        "sidebar-box-shadow": "0 0 10px #FFFFFF",
    },
    "Blue": {
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
        "background-color": "#000000",
        "color": "#FFA500",
        "button-background-color": "#FFA500",
        "button-color": "#000000",
        "button-box-shadow": "0 0 10px #FFA500",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#FFA500",
        "sidebar-box-shadow": "0 0 10px #FFA500",
    },
    "Neon": {
        "background-color": "#000000",
        "color": "#00FFFF",
        "button-background-color": "#00FFFF",
        "button-color": "#000000",
        "button-box-shadow": "0 0 20px #00FFFF",
        "sidebar-background-color": "#0D1117",
        "sidebar-color": "#00FFFF",
        "sidebar-box-shadow": "0 0 20px #00FFFF",
    },
}

# Set the initial theme
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

# Add a theme selection dropdown menu to the sidebar
selected_theme = st.sidebar.selectbox("🎨 Choisissez un thème", list(themes.keys()), index=0)
update_theme(selected_theme)


st.title("Bienvenue sur Synapse AI")

st.markdown("""
**Synapse AI** est une plateforme de collaboration créative et de productivité augmentée, assistée par une intelligence artificielle avancée. Que vous soyez un créateur, un chercheur ou une entreprise, Synapse AI est là pour vous aider à réaliser vos projets.
""")


# Initialiser le contexte de la conversation
if 'context' not in st.session_state:
    st.session_state.context = []

# Zone de conversation
conversation = st.empty()

def update_conversation():
    conversation.text_area("📜 **Historique de la conversation**", 
                           value="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.context]),
                           height=300)

# Onglets pour choisir entre chat vocal et écrit
tab1, tab2, tab3 = st.tabs(["💬 Chat Écrit", "🎙️ Chat Vocal"," Assistant IA"])

with tab1:
    # Zone de saisie de texte
    user_input = st.text_input("Écrivez votre message ici")
    
    # Déplacer la case à cocher avant le bouton d'envoi
    read_aloud = st.checkbox("🔊 Lire la réponse à voix haute")

    if st.button("Envoyer"):
        if user_input:
            # Analyser le sentiment
            sentiment = analyze_sentiment(user_input)
            st.write(f"**Sentiment détecté** : {sentiment}")

            # Interroger ChatGPT
            response = ask_openai(user_input, st.session_state.context)
            st.write(f"**Agent** : {response}")

            # Ajouter au contexte
            st.session_state.context.append({"role": "user", "content": user_input})
            st.session_state.context.append({"role": "assistant", "content": response})

            # Mettre à jour la zone de conversation
            update_conversation()

            # Lire la réponse à voix haute si la case est cochée
            if read_aloud:
                audio_fp = speak_text(response)
                st.audio(audio_fp, format='audio/mp3')

with tab2:
    # Bouton pour démarrer la reconnaissance vocale
    if st.button("🎙️ Parler à l'agent"):
        with st.spinner("🔊 Écoute en cours..."):
            recognized_text = recognize_speech()
            if recognized_text:
                st.write(f"**Vous avez dit** : {recognized_text}")

                if "arrêter" in recognized_text.lower():
                    st.warning("Arrêt de l'agent vocal.")
                    audio_fp = speak_text("Au revoir ! J'espère vous revoir bientôt.")
                    st.audio(audio_fp, format='audio/mp3')
                else:
                    # Analyser le sentiment
                    sentiment = analyze_sentiment(recognized_text)
                    st.write(f"**Sentiment détecté** : {sentiment}")

                    # Interroger ChatGPT
                    response = ask_openai(recognized_text, st.session_state.context)
                    st.write(f"**Agent** : {response}")

                    # Ajouter au contexte
                    st.session_state.context.append({"role": "user", "content": recognized_text})
                    st.session_state.context.append({"role": "assistant", "content": response})

                    # Mettre à jour la zone de conversation
                    update_conversation()

                    # Synthèse vocale de la réponse
                    audio_fp = speak_text(response)
                    st.audio(audio_fp, format='audio/mp3')



with tab3:

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
                        {"role": "system", "content": "Vous êtes un assistant utile."},
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



# Bouton pour effacer l'historique
if st.button("🗑️ Effacer l'historique"):
    st.session_state.context = []
    update_conversation()
    st.success("Historique effacé !")

# Afficher des statistiques
st.sidebar.title("📊 Statistiques")

total_messages = len(st.session_state.context) - 1  # Exclure le message système
average_length = sum(len(msg['content']) for msg in st.session_state.context if msg['role'] != "system") / total_messages if total_messages > 0 else 0
st.sidebar.write(f"**Nombre de messages** : {total_messages}")
st.sidebar.write(f"**Longueur moyenne des réponses** : {average_length:.0f} caractères")

# Easter egg
if st.sidebar.button("🎁 Surprise !"):
    jokes = [
        "Pourquoi les robots ne prennent-ils jamais de vacances ? Parce qu'ils ont déjà trop de vis !",
        "Comment s'appelle un robot qui fait toujours la même chose ? Un automate.",
        "Que dit un robot quand il tombe en panne ? 'J'ai un bug-out-bag !'",
    ]
    joke = random.choice(jokes)
    st.sidebar.write(joke)
    audio_fp = speak_text(joke)
    st.audio(audio_fp, format='audio/mp3')


st.sidebar.write('---')
# Ajouter un droit d'auteur
now = datetime.datetime.now()
st.sidebar.write(f"Date : {now.strftime('%Y-%m-%d')} Heure : {now.strftime('%H:%M')}")
st.sidebar.write(f"© {now.year} Salam & Nesrine")

