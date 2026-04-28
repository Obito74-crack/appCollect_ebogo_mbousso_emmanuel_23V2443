import folium
import plotly.express as px
import pandas as pd

# Coordonnées approximatives des 10 régions du Cameroun
REGION_COORDS = {
    "Centre": [3.8480, 11.5021],
    "Littoral": [4.0511, 9.7679],
    "Ouest": [5.4801, 10.4217],
    "Sud": [2.9019, 11.1504],
    "Est": [4.5773, 13.6845],
    "Adamaoua": [7.3227, 13.5838],
    "Nord": [9.3000, 13.3999],
    "Extrême-Nord": [10.5910, 14.3218],
    "Nord-Ouest": [5.9587, 10.1555],
    "Sud-Ouest": [4.1558, 9.2407]
}

def create_map(df_totals_region):
    """
    Crée une carte Folium du Cameroun avec des marqueurs proportionnels à la production.
    """
    # Centrer la carte sur le Cameroun
    m = folium.Map(location=[5.3, 12.3], zoom_start=6, tiles="CartoDB positron")
    
    if df_totals_region.empty:
        return m
        
    # Calculer un facteur d'échelle pour les cercles
    max_quantite = df_totals_region['quantite'].max()
    
    for _, row in df_totals_region.iterrows():
        region = row['region']
        quantite = row['quantite']
        if region in REGION_COORDS and quantite > 0:
            # Rayon dynamique (min 5, max 30)
            radius = 5 + (quantite / max_quantite) * 25 if max_quantite > 0 else 5
            
            folium.CircleMarker(
                location=REGION_COORDS[region],
                radius=radius,
                popup=f"<b>{region}</b><br>Production: {quantite:.2f} t",
                tooltip=region,
                color="#006400",
                fill=True,
                fillColor="#228B22",
                fillOpacity=0.7
            ).add_to(m)
            
    return m

def create_culture_chart(df_totals_culture):
    """Crée un pie chart Plotly pour la répartition par culture."""
    if df_totals_culture.empty:
        # Graphe vide de fallback
        fig = px.pie(title="Répartition par culture (Aucune donnée)")
        return fig
        
    fig = px.pie(
        df_totals_culture, 
        values='quantite', 
        names='culture', 
        title="Répartition de la Production par Culture",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_season_culture_chart(df_season_culture):
    """Crée un bar chart groupé pour comparer saison vs culture."""
    if df_season_culture.empty:
        fig = px.bar(title="Comparaison Saisons/Cultures (Aucune donnée)")
        return fig
        
    fig = px.bar(
        df_season_culture, 
        x="culture", 
        y="quantite", 
        color="saison", 
        barmode="group",
        title="Production par Culture et Saison",
        labels={"quantite": "Quantité (Tonnes)", "culture": "Culture"},
        color_discrete_map={"Saison Sèche": "#FFA07A", "Saison des Pluies": "#20B2AA"}
    )
    return fig
