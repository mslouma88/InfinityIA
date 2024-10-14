import os
from typing import List
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document

# Charger les variables d'environnement
load_dotenv()

def load_documents(uploaded_files: List[object]) -> List[Document]:
    """
    Charge les documents téléchargés (PDF et TXT) et retourne une liste de documents.
    """
    documents = []
    for file in uploaded_files:
        try:
            file_path = f"/tmp/{file.name}"
            with open(file_path, "wb") as f:
                f.write(file.getvalue())
            
            if file.type == "application/pdf":
                loader = PyPDFLoader(file_path)
            elif file.type == "text/plain":
                loader = TextLoader(file_path)
            else:
                print(f"Type de fichier non supporté : {file.type}")
                continue
            
            docs = loader.load()
            documents.extend(docs)
            os.remove(file_path)
        except Exception as e:
            print(f"Erreur lors du chargement du fichier {file.name} : {e}")
    return documents

def search_documents(uploaded_files: List[object], question: str) -> str:
    """
    Recherche dans les documents téléchargés et retourne une réponse basée sur la question posée.
    """
    try:
        # Charger les documents
        documents = load_documents(uploaded_files)
        if not documents:
            return "Aucun document valide téléchargé."

        # Diviser les documents en chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # Initialiser les embeddings
        embeddings = OpenAIEmbeddings()
        
        # Créer l'index vectoriel avec FAISS
        vector_store = FAISS.from_documents(texts, embeddings)
        
        # Initialiser le modèle LLM avec ChatOpenAI
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        
        # Créer une chaîne de questions-réponses avec récupération
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        
        # Obtenir la réponse
        result = qa({"query": question})
        answer = result['result']
        sources = [doc.metadata.get('source', 'Source inconnue') for doc in result['source_documents']]
        
        return f"Réponse : {answer}\n\nSources : {', '.join(set(sources))}"

    except Exception as e:
        return f"Une erreur est survenue lors de la recherche dans les documents : {e}"