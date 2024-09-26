# FastAPI Application avec Docker

## Description

Ce projet est une API FastAPI simple qui expose deux routes :
- `GET /`: Retourne un message d'accueil `"hello world!"`.
- `GET /file`: Télécharge un fichier CSV depuis une URL externe et l'enregistre localement.

L'application utilise Docker pour être déployée, et un volume lié est monté pour stocker les fichiers de données.

## Structure des fichiers

- `main.py`: Fichier Python contenant l'API FastAPI.
- `Dockerfile`: Fichier Docker pour containeriser l'application.
- `requirements.txt`: Liste des dépendances Python.
- `data/databse.csv`: Chemin où le fichier téléchargé sera stocké.

## Prérequis

Assurez-vous d'avoir installé les outils suivants sur votre machine :
- **Docker** : Pour construire et exécuter les conteneurs.
- **Python 3.9** ou supérieur : Si vous souhaitez exécuter l'application en local (en dehors de Docker).

## Installation

### 2. Construire l'image Docker

Utilisez la commande suivante pour construire l'image Docker :

```bash
docker build -t tp .
```

### 3. Exécuter le conteneur Docker

```bash
docker run -d -p 8000:80 -v /<chemin de votre dossier >/tp1/data:/app/data --name tp tp
```

- L'application sera accessible via **http://localhost:8000**.
- Les fichiers téléchargés seront stockés dans le répertoire local `data` sur votre machine.

## Utilisation de l'API

### Route principale

- **GET `/`**
    - Exemple de requête en ligne de commande :
    ```bash
    curl http://localhost:8000/
    ```
    - Réponse :
    ```json
    {
      "home": "hello world!"
    }
    ```

### Télécharger un fichier CSV

- **GET `/file`**
    - Cette route télécharge un fichier CSV depuis une URL externe (https://raw.githubusercontent.com/france-connect/data-provider-example/refs/heads/master/database.csv) et l'enregistre localement dans le répertoire `/app/data`.
    - Exemple de requête en ligne de commande :
    ```bash
    curl http://localhost:8000/file
    ```
    - Réponse en cas de succès :
    ```json
    {
      "file": "data/databse.csv"
    }
    ```
    - Réponse en cas d'erreur :
    ```json
    {
      "file": "il y a un probleme",
      "status": 404
    }
    ```

## Détails techniques

### Dockerfile

```dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY ./main.py /app/
COPY ./requirements.txt /app/
COPY /data /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

- L'image est basée sur **tiangolo/uvicorn-gunicorn-fastapi:python3.9**.
- Les fichiers `main.py` et `requirements.txt` sont copiés dans le conteneur.
- Le fichier CSV est stocké dans un volume lié.

### Fichier `requirements.txt`

```
fastapi
uvicorn
requests
```

- **fastapi** : Framework web utilisé pour créer l'API.
- **uvicorn** : Serveur ASGI rapide utilisé pour déployer l'API.
- **requests** : Bibliothèque pour effectuer des requêtes HTTP, utilisée pour télécharger le fichier CSV.

## Commandes Docker supplémentaires

### Arrêter le conteneur

```bash
docker stop tp
```

### Supprimer le conteneur

```bash
docker rm tp
```

### Supprimer l'image Docker

```bash
docker rmi tp
```

---
