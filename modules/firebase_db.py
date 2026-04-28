import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import uuid

# Mock storage over app restarts if we need to mock it, best kept in session_state,
# but for a generic module we'll set up a global mock dict here for fallback
MOCK_DB = []

def init_firebase():
    """Charge la configuration Firebase depuis Streamlit Secrets, .env, ou un fichier JSON."""
    if not firebase_admin._apps:
        # 1. Essayer Streamlit Secrets
        if "firebase" in st.secrets:
            cred_dict = dict(st.secrets["firebase"])
            # Format correction for private_key if needed
            if "\\n" in cred_dict.get("private_key", ""):
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            try:
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
            except Exception as e:
                print(f"Erreur init Streamlit secrets Firebase: {e}")
                
        # 2. Essayer les variables d'environnement (via dotenv)
        elif os.environ.get("FIREBASE_PROJECT_ID"):
            cred_dict = {
                "type": os.environ.get("FIREBASE_TYPE", "service_account"),
                "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
                "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
                "auth_uri": os.environ.get("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": os.environ.get("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
                "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL")
            }
            try:
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
            except Exception as e:
                print(f"Erreur init ENV Firebase: {e}")
                
    else:
        return firestore.client()
        
    # Return None to indicate fallback mock mode
    return None

def add_production(db, data):
    """Ajoute une entrée dans la collection 'production_agricole'."""
    data["timestamp"] = datetime.now().isoformat()
    # Si db est None, on utilise le mock
    if db is None:
        doc_id = str(uuid.uuid4())
        data["id"] = doc_id
        if "mock_db" not in st.session_state:
            st.session_state.mock_db = []
        st.session_state.mock_db.append(data)
        return doc_id
        
    # Sinon on utilise Firebase Firestore
    try:
        doc_ref = db.collection("production_agricole").document()
        doc_ref.set(data)
        return doc_ref.id
    except Exception as e:
        st.error(f"Erreur Firebase : {e}")
        return None

def get_all_productions(db):
    """Récupère toutes les productions."""
    if db is None:
        return st.session_state.get("mock_db", [])
        
    try:
        docs = db.collection("production_agricole").stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        st.error(f"Erreur Firebase lecture : {e}")
        return []
