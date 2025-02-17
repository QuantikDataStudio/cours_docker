# Analyseur de Données CSV avec Streamlit et Docker

Une application web permettant d'analyser des fichiers CSV et de générer des rapports détaillés avec historisation dans une base de données PostgreSQL.

## 📑 Sommaire

1. [Présentation du Projet](#-présentation-du-projet)
2. [Fonctionnalités](#-fonctionnalités)
3. [Technologies Utilisées](#-technologies-utilisées)
4. [Installation](#-installation)
5. [Architecture et Code](#-architecture-et-code)
6. [Utilisation](#-utilisation)
7. [Configuration](#-configuration)
8. [Notes Techniques](#-notes-techniques)
9. [Fichier `.dockerignore`](#-fichier-dockerignore)

## 🎯 Présentation du Projet

Cette application permet aux utilisateurs de télécharger des fichiers CSV pour générer automatiquement des rapports d'analyse détaillés. Les rapports sont sauvegardés et peuvent être consultés ultérieurement via l'interface web.

## ✨ Fonctionnalités

- Upload de fichiers CSV avec détection automatique de l'encodage
- Génération de rapports d'analyse détaillés avec ydata-profiling
- Historisation des analyses dans une base de données PostgreSQL
- Consultation et téléchargement des rapports précédents
- Interface utilisateur intuitive avec Streamlit
- Visualisation des informations de la base de données

## 🛠 Technologies Utilisées

- **Streamlit**: Framework pour l'interface utilisateur
- **Docker & Docker Compose**: Conteneurisation de l'application
- **PostgreSQL**: Base de données pour l'historisation
- **Python**: Langage de programmation
- **pandas**: Manipulation des données
- **ydata-profiling**: Génération des rapports d'analyse

## 📥 Installation

1. Clonez le dépôt :

```bash
git clone [url-du-repo]
cd tp-streamlit-docker
```

2. Lancez l'application avec Docker Compose :

```bash
docker-compose up --build
```

3. Accédez à l'application :

```
http://localhost:8501
```

## 🔍 Architecture et Code

### Structure du Projet

```
tp-streamlit-docker/
├── app.py              # Application Streamlit principale
├── Dockerfile         # Configuration Docker
├── docker-compose.yml # Configuration Docker Compose
├── init.sql          # Initialisation de la base de données
├── requirements.txt   # Dépendances Python
└── analyses/         # Dossier de stockage des rapports
```

### Points Techniques Importants

#### Gestion des Encodages

```python
# Détection automatique de l'encodage des fichiers CSV
encodings = ["utf-8", "latin1", "iso-8859-1", "cp1252"]
for encoding in encodings:
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding)
        break
    except UnicodeDecodeError:
        continue
```

#### Sauvegarde des Rapports

```python
# Génération d'un chemin unique pour chaque rapport
timestamp = datetime.now().strftime('%Y%m%d_%H%m%S_%f')
report_dir = pathlib.Path("analyses") / timestamp
report_dir.mkdir(parents=True, exist_ok=True)
```

#### Connexion à la Base de Données

```python
# Utilisation de context managers pour la gestion des connexions
def init_connection():
    return psycopg2.connect(DATABASE_URL)

def run_query(query):
    with init_connection() as conn:
        return pd.read_sql_query(query, conn)
```

## 💡 Utilisation

### Page "Upload et Analyse"

1. Sélectionnez un fichier CSV à analyser
2. Attendez la génération du rapport
3. Consultez les résultats de l'analyse
4. Le rapport est automatiquement sauvegardé

### Page "Analyses Historiques"

- Consultez la liste des analyses précédentes
- Visualisez les rapports générés
- Téléchargez les rapports au format HTML

### Page "Info Base de données"

- Visualisez les informations techniques de la base de données PostgreSQL

## ⚙️ Configuration

Les variables d'environnement sont configurées dans le `docker-compose.yml` :

- `POSTGRES_USER`: Utilisateur de la base de données
- `POSTGRES_PASSWORD`: Mot de passe de la base de données
- `POSTGRES_DB`: Nom de la base de données
- `DATABASE_URL`: URL de connexion à la base de données

## 📝 Notes Techniques

- Les rapports sont générés avec ydata-profiling en mode "minimal" pour optimiser les performances
- L'application utilise des volumes Docker pour persister les données :
  - `postgres_data`: Pour les données PostgreSQL
  - `./analyses`: Pour les rapports générés
- La détection automatique de l'encodage supporte UTF-8, Latin1, ISO-8859-1 et CP1252
- Les connexions à la base de données sont gérées avec des context managers pour éviter les fuites de ressources
- L'application est conteneurisée pour faciliter le déploiement et assurer la cohérence des environnements

## ⛔️ Fichier `.dockerignore`

Le fichier `.dockerignore` permet d'exclure certains fichiers ou répertoires du contexte de build de l'image Docker. Dans notre cas, les éléments suivants sont ignorés :

- Le répertoire `tpStream/` et tous ses sous-répertoires (`tpStream/**`)
- Le fichier `docker-compose.yml`
- Le fichier `readme.md`
- Le fichier `init.sql`

Cela signifie que ces fichiers ne seront pas copiés dans l'image Docker lors de la construction.
