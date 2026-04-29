import pandas as pd

def parse_to_dataframe(data_list):
    """Convertit la liste de dictionnaires en DataFrame Pandas Pandas sécurisé."""
    if not data_list:
        # Retourne un DF vide avec les bonnes colonnes si pas de données
        return pd.DataFrame(columns=["id", "cooperative", "region", "annee", "saison", "culture", "quantite", "timestamp"])
    
    df = pd.DataFrame(data_list)
    # Assurer que 'quantite' est numérique
    if 'quantite' in df.columns:
        df['quantite'] = pd.to_numeric(df['quantite'], errors='coerce').fillna(0)
    
    return df

def get_totals_by_region(df):
    """Calcule le total de production par région."""
    if df.empty or 'region' not in df.columns or 'quantite' not in df.columns:
        return pd.DataFrame(columns=["region", "quantite"])
        
    return df.groupby('region', as_index=False)['quantite'].sum()

def get_totals_by_culture(df):
    """Calcule le total par type de culture."""
    if df.empty or 'culture' not in df.columns or 'quantite' not in df.columns:
        return pd.DataFrame(columns=["culture", "quantite"])
        
    return df.groupby('culture', as_index=False)['quantite'].sum()

def get_totals_by_season_and_culture(df):
    """Calcule le total comparatif saison vs culture."""
    if df.empty or 'culture' not in df.columns or 'saison' not in df.columns or 'quantite' not in df.columns:
        return pd.DataFrame(columns=["saison", "culture", "quantite"])
        
    return df.groupby(['saison', 'culture'], as_index=False)['quantite'].sum()

def get_csv_export(df):
    """Genère un CSV en bytes pour le téléchargement Streamlit."""
    return df.to_csv(index=False).encode('utf-8')

def get_evolution_by_season_year(df):
    """Calcule l'évolution totale de la production chronologiquement (Année + Saison)."""
    if df.empty or 'annee' not in df.columns or 'saison' not in df.columns or 'quantite' not in df.columns:
        return pd.DataFrame(columns=["periode", "quantite"])
        
    # Création d'une variable chronologique
    df_temp = df.copy()
    # Ordonner pour que Saison Sèche apparaisse avant Saison des Pluies
    # Mais ici on concaténera juste proprement
    df_temp['periode'] = df_temp['annee'].astype(str) + " (" + df_temp['saison'].str.replace('Saison ', '') + ")"
    
    # Grouper par annee et saison d'abord pour garder un ordre correct
    grouped = df_temp.groupby(['annee', 'saison', 'periode'], as_index=False)['quantite'].sum()
    
    # Tri (2024, Saison Sèche, puis 2024, Saison des Pluies, etc.)
    # Pour trier Sèche avant Pluies
    grouped['saison_order'] = grouped['saison'].map({"Saison Sèche": 1, "Saison des Pluies": 2})
    grouped = grouped.sort_values(by=['annee', 'saison_order'])
    
    return grouped[['periode', 'quantite']]
