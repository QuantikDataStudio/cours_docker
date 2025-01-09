## Démarrage du projet

1. Clonez le dépôt :

   ```bash
   git clone <url repo>
   ```

2. Construisez et démarrez les conteneurs :

   ```bash
   docker-compose up --build -d
   ```

3. Accédez à l'API à l'adresse suivante : [http://localhost:8080/file](http://localhost:8080/file)

## Fonctionnalités

- **Importation de fichiers CSV** : L'API permet de télécharger un fichier CSV depuis une URL et de l'enregistrer localement.
- **Insertion dans PostgreSQL** : Les données du fichier CSV sont insérées dans une table PostgreSQL.

## Logs

Les logs de l'application sont enregistrés dans le fichier `app.log`.

## Accès à pgAdmin

Vous pouvez accéder à pgAdmin à l'adresse suivante : [http://localhost:5050](http://localhost:5050) avec les identifiants que vous avez définis dans le fichier `.env`.

## Aide

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur le discord

## License

formation @ada-study
