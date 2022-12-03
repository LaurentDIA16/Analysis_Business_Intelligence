# IA_AnalysisBusinessIntelligence

## Sur MacOS
## Installation
- Installer un environnement virtuel : "python3 -m venv .env"
- Lancer l'environnement virtuel : "source .env/bin/activate"
- Installer les différents packages (Django, ...) : "pip install -r requirements.txt"
- Créer la base de donnée sur postgres avec les infos disponible dans le fichier settings.py
- Créer un nouveau login dans postgres avec nom moni et mdp moni, mettre tout les privilèges
- Effectuer les premières migrations, dans le terminal taper : "cd src" puis "python manage.py makemigrations" et "python manage.py migrate"

## Lancer serveur Django
- Vérifier que l'environnement virtuel est lancé et que vous êtes bien dans le dossier 'src' : "python manage.py runserver"

## Le projet
Réalisation d'un proof of concept (PoC) dans le cadre d’un projet de dashboard d’aide à la décision pour un client. J'ai accès à un fichier de données brutes, matérialisant un export depuis les bases de données opérationnelles du client.

Ce fichier CSV alimentera ma base analytique et tient lieu de situation initiale. Les CSV des mois suivants me seront régulièrement transmis.

IMPORTANT. Le dashboard - en accès retreint - devra permettre à l’utilisateur de déclencher son import

- avec suffisamment de feedback pour comprendre les décisions ETL automatisées ou semi automatisées proposées
- de façon cumulative : d’autres CSV vont arriver

Le dashboard comprendra obligatoirement ces éléments suivants :

- un graphique précisant la répartition des ventes par produit
- un graphique précisant la répartition des ventes par région
- un dernier graphique précisant la répartition des ventes par région et par produit