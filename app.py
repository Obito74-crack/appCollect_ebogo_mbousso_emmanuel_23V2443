import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import os
import sys

# Ajouter le répertoire courant au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import firebase_db, data_process, visualizations

# Configuration de la page
st.set_page_config(
    page_title="Agricollect - Cameroun",
    page_icon="🌾",
    layout="wide"
)

# Initialisation de Firebase
db = firebase_db.init_firebase()

# Variables statiques pour les formulaires
REGIONS = ["Centre", "Littoral", "Ouest", "Sud", "Est", "Adamaoua", "Nord", "Extrême-Nord", "Nord-Ouest", "Sud-Ouest"]
SAISONS = ["Saison Sèche", "Saison des Pluies"]
CULTURES = ["Maïs", "Sorgho", "Manioc", "Mil", "Cacao"]

def main():
    st.sidebar.title("🌾 Agricollect CM")
    st.sidebar.markdown("Plateforme de suivi de la production agricole au Cameroun.")
    
    # Navigation
    page = st.sidebar.radio("Navigation", ["Saisie (Formulaire)", "Dashboard & Données", "Carte & Analytique"])
    
    if page == "Saisie (Formulaire)":
        show_form_page()
    elif page == "Dashboard & Données":
        show_dashboard_page()
    elif page == "Carte & Analytique":
        show_analytics_page()
        
    st.sidebar.markdown("---")
    st.sidebar.info("Développé pour l'aide à la décision.")

def show_form_page():
    st.title("Déclaration de Production")
    st.markdown("Veuillez remplir le formulaire ci-dessous pour déclarer la récolte de votre coopérative.")
    
    # Détection mode Mock
    if db is None:
        st.warning("Mode développement (Mock) activé. Les données seront perdues au redémarrage complet de l'application.")
        
    with st.form("form_production", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            coop_name = st.text_input("Nom de la coopérative", placeholder="Ex: Coopérative de Mbankomo")
            region = st.selectbox("Région", REGIONS)
            saison = st.selectbox("Saison", SAISONS)
            
        with col2:
            culture = st.selectbox("Type de culture", CULTURES)
            quantite = st.number_input("Quantité produite (en Tonnes)", min_value=0.0, step=0.5, format="%.2f")
            
        submit = st.form_submit_button("Soumettre la déclaration")
        
        if submit:
            if not coop_name.strip():
                st.error("Le nom de la coopérative est obligatoire.")
            elif quantite <= 0:
                st.error("La quantité doit être supérieure à 0.")
            else:
                data = {
                    "cooperative": coop_name,
                    "region": region,
                    "saison": saison,
                    "culture": culture,
                    "quantite": quantite
                }
                
                # Sauvegarde Firebase (ou Mock)
                doc_id = firebase_db.add_production(db, data)
                
                if doc_id:
                    st.success("✅ Déclaration enregistrée avec succès !")
                else:
                    st.error("❌ Une erreur est survenue lors de l'enregistrement.")

def show_dashboard_page():
    st.title("Dashboard Agricole")
    st.markdown("Consultez toutes les données collectées sur le terrain.")
    
    # Récupérer les données
    raw_data = firebase_db.get_all_productions(db)
    df = data_process.parse_to_dataframe(raw_data)
    
    if df.empty:
        st.info("Aucune donnée disponible pour le moment.")
        return
        
    # Mettre en forme pour l'affichage : tri par date décroissante
    df_display = df.sort_values(by="timestamp", ascending=False)
    # Réordonner les colonnes optionnel
    columns = ["cooperative", "region", "saison", "culture", "quantite", "timestamp"]
    if all(col in df_display.columns for col in columns):
        df_display = df_display[columns]
        
    # Affichage tableur
    st.dataframe(df_display, use_container_width=True)
    
    # Boutons d'export
    st.subheader("Exporter les données")
    csv_bytes = data_process.get_csv_export(df_display)
    st.download_button(
        label="📥 Télécharger en CSV",
        data=csv_bytes,
        file_name="productions_cameroun.csv",
        mime="text/csv",
    )

def show_analytics_page():
    st.title("Analytique et Cartographie")
    
    raw_data = firebase_db.get_all_productions(db)
    df = data_process.parse_to_dataframe(raw_data)
    
    if df.empty:
        st.info("Aucune donnée disponible pour les visualisations.")
        return
        
    st.subheader("Carte de la Production par Région (Tonnes)")
    
    # Preparer dataframe pour Folium
    df_regions = data_process.get_totals_by_region(df)
    
    # Créer et afficher la carte
    m = visualizations.create_map(df_regions)
    st_folium(m, height=500, width=800, returned_objects=[])
    
    st.markdown("---")
    
    st.subheader("Graphiques Analytiques")
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart des cultures
        df_cultures = data_process.get_totals_by_culture(df)
        fig_pie = visualizations.create_culture_chart(df_cultures)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        # Bar chart Saisons vs Cultures
        df_saison_culture = data_process.get_totals_by_season_and_culture(df)
        fig_bar = visualizations.create_season_culture_chart(df_saison_culture)
        st.plotly_chart(fig_bar, use_container_width=True)

if __name__ == "__main__":
    main()
