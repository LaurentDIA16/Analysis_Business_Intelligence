# IA_AnalysisBusinessIntelligence

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

## Documentation du projet

Voir document `BRIEF 1C`

Les 2 fichiers CSV data sont les fichiers utilisés dans la réalisation de ce projet, ils sont uploadés au travers de la page "import"

## Livrables
  
  Les fonctionnalités suivantes sont à réaliser en priorité :
  
- nettoyer les données brutes (suppression des doublons et “faux”, standardisation, etc)
- concevoir et paramétrer la base de données analytique
- récupérer les données en base nécessaires pour le dashboard
- développer les interfaces et les graphiques du dashboard
  
Dossier technique

## Installation

- Installer un environnement virtuel :

  - Windows :

    `py -m venv .env`
  
  - Linux ou Mac OS :
  
    `python3 -m venv .env` ou `python -m venv .env`
  
- Lancer l'environnement virtuel :

  - Windows :

    `.env\Scripts\activate`
  
  - Linux ou Mac OS :
  
    `source .env/bin/activate`
  
- Installer les différents packages (Django, ...) :

  `pip install -r requirements.txt`

- Créer la base de données sur PostgreSQL :

  - Paramètres de configuration :
  
    - Name : DB_Analysis_Business_Intelligence
    - User : moni
    - Password : moni
  
- Effectuer les premières migrations :
  
  - Windows :

    `py manage.py makemigrations`

    `py manage.py migrate`
  
  - Linux ou Mac OS :

    `python3 manage.py makemigrations` ou `python manage.py makemigrations`

    `python3 manage.py migrate` ou `python manage.py migrate`

- Lancer le serveur Django

  - Vérifier que l'environnement virtuel est lancé et que vous êtes bien dans le dossier `src` :

    - Windows :
  
      `py manage.py runserver`

    - Linux ou Mac OS :
  
      `python3 manage.py runserver` ou `python manage.py runserver`
