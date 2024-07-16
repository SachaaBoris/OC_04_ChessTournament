# OC_04_ChessTournament  :chess_pawn:  
  
WIP !!!  :construction_worker:  
  
# ● Description du projet  
Ce programme répond à la demande d'une amie pour aider son club d'échecs dans la gestion de ses tournois.  
L'objectif est de pouvoir sauvegarder et maintenir une base de données de joueurs et une base de données de tournois. Il permet d'ajouter des joueurs, editer des joueurs, lister les joueurs, créer des tournois, ajouter des joueurs à un tournoi, rentrer les scores de chaque match, pour chaque round d'un tournoi, reprendre un tournoi laissé en suspend, suivre les scores des joueurs, lister les tournois et revoir les données enregistrées des tournois passés ou en cours.
  
# ● Comment installer et démarrer l'application  
1. Prérequis :  
Avoir Python 3 installé  
Avoir téléchargé et dézipé l'archive du projet sur votre disque dur,  
Ou clonez le repo avec cette commande :  
    ```
    git clone https://github.com/SachaaBoris/OC_04_ChessTournament.git path\to\your\folder\here  
    ```
  
2. Installer l'environnement virtuel :  
    Depuis votre console favorite, naviguez jusqu'au repertoire de l'application  
    Pour créer l'environnement virtuel rentrez la ligne de commande : `py -m venv .chess/venv`  
    Activez ensuite l'environnement virtuel en rentrant la commande : `chess\venv\Scripts\activate`  
    Installer les requirements du projet avec la commande : `py -m pip install -r requirements.txt`  
  
3. Démarrer le script :  
    Toujours dans la console et à la racine du projet, executez le script avec la commande : `py chess`  
  
4. Exporter un nouveau rapport flake8 *(optionnel)* :  
    Toujours dans la console et à la racine du projet, executez la commande :  
    ```
    py -m flake8 chess --exclude venv --format=html --htmldir=flake-report --max-line-length=119
    ```
    Flake va parcourir le projet et exporter un rapport html dans le dossier flake-report,  
    pour le visionner, lancez l'index.htm dans votre navigateur favoris.  
  
# ● Caractéristiques  
Un menu simple avec en-têtes pour naviguer efficacement sans jamais être perdu  
Un affichage clair des éventuelles erreurs ou mauvais inputs  
Un systeme de base de données robuste avec sauvegarde automatique à chaque changement  
Les dates de débuts et de fin de tournoi et de matchs sont entrées automatiquement  
Possibilité de laisser un ou plusieurs tournois en suspend et de les reprendre plus tard  
Verifications et formatage d'inputs pour minimiser les erreurs et avoir des données cohérentes  
Ajout de joueurs dans un tournoi depuis la bdd géré de façon ergonomique  
Visibilité des rapports et des pages grâce à des tableaux lisibles  
Developpement MVC orienté objets pour faciliter la maintenance du code  
  
---  
  
[![CC BY 4.0][cc-by-shield]][cc-by]  
  
This work is licensed under a [Creative Commons Attribution 4.0 International License][cc-by].  
  
[cc-by]: http://creativecommons.org/licenses/by/4.0/  
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg  
