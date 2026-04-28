# Agricollect CM - Application Streamlit

Cette application répond au cahier des charges pour la collecte et la visualisation de la production agricole dans les 10 régions du Cameroun.

## Architecture & Technologies
- **Python 3 / Streamlit** : Interface utilisateur rapide et Data App.
- **Firebase Firestore** : Base de données NoSQL hébergée sur le cloud.
- **Pandas** : Traitement et agrégation des données.
- **Plotly & Folium** : Graphiques analytiques et Cartographie.

## Utilisation locale

Pour lancer l'application sur votre machine en mode "Développement" (avec base de données en mémoire "Mock" si Firebase n'est pas configuré) :

1. Activez votre environnement virtuel ou assurez-vous d'avoir Python >= 3.9
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez l'application :
   ```bash
   streamlit run app.py
   ```

## Configuration Firebase (Production)

Si vous voulez connecter votre base de données :
1. Créez un projet sur Firebase Console, ajoutez "Firestore Database" en mode de test ou production.
2. Allez dans Paramètres du projet > Comptes de service > Générez une nouvelle clé privée (fichier JSON).
3. Ouvrez `.streamlit/secrets.toml.example`, remplissez avec les valeurs de votre JSON, et renommez ce fichier en `secrets.toml` dans le dossier `.streamlit/`.

## Hébergement Gratuit (24/7) sur Streamlit Community Cloud

Pour avoir une URL publique accessible en permanence et héberger l'application gratuitement :

1. Poussez ce dossier `agricollect-streamlit` sur un dépôt (repository) public ou privé sur **GitHub**.
2. Allez sur [Streamlit Community Cloud](https://share.streamlit.io/) et connectez-vous avec votre compte GitHub.
3. Cliquez sur **"New app"**.
4. Sélectionnez votre dépôt (Repository), la branche (ex: `main`), et le "Main file path" qui doit être `app.py`.
5. Si vous utilisez Firebase : Avant de cliquer sur "Deploy", cliquez sur **"Advanced settings"** et copiez-collez le contenu de votre fichier `secrets.toml` dans la zone **"Secrets"**.
6. Cliquez sur **"Deploy!"**. 

Votre application sera en ligne, accessible via un lien public partageable avec votre professeur, garantie de fonctionnement 24/7 !
