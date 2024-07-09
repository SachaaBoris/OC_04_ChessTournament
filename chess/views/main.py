import os
import time
from prettytable import PrettyTable

class MainView:
    ''' Vue principale '''

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def menu_header(self, index):
        texts = {
            0: " \n",
            1: "Menu Principal\n",
            2: "Gestion des joueurs\n",
            3: "Gestion des tournois\n",
            4: "Génération de rapports\n",
            5: "Ajout de joueur\n",
            6: "Modification de joueur\n",
            7: "Préparer un tournoi\n",
            8: "Tournoi en cours\n",
            9: "Liste des joueurs\n",
            10: "Liste des tournois\n",
            11: "Nom, ville & date d'un tournoi\n",
            12: "Liste des joueurs d'un tournoi\n",
            13: "Liste de tous les matchs d'un tournoi\n"            
        }
        message = texts.get(index, "Invalid header index")
        print(f"Chess Tournament Manager v0.1\n" + f"{message}")
    
    def main_menu(self):
        self.menu_header(1)
        texts = [
            "1 - Gestion des joueurs",
            "2 - Gestion des tournois",
            "3 - Générer des rapports",
            "4 - Quitter\n"
        ]
        for text in texts:
            print(f"{text}")
    
    def player_menu(self):
        self.menu_header(2)
        texts = [
            "1 - Ajouter un joueur",
            "2 - Modifier un joueur",
            "3 - Voir la liste des joueurs",
            "4 - Revenir au menu principal\n"
        ]
        for text in texts:
            print(f"{text}")

    def tournament_menu(self):
        self.menu_header(3)
        texts = [
            "1 - Préparer un tournoi",
            "2 - Lancer / Reprendre un tournoi",
            "3 - Voir la liste des tournois",
            "4 - Revenir au menu principal\n"
        ]
        for text in texts:
            print(f"{text}")

    def report_menu(self):
        self.menu_header(4)
        texts = [
            "1 - Liste des joueurs enregistrés",
            "2 - Liste des tournois",
            "3 - Nom, ville & date d'un tournoi spécifique",
            "4 - Lister tous les joueurs d'un tournoi spécifique",
            "5 - Lister tous les matchs de tous les tours d'un tournoi spécifique",
            "6 - Revenir au menu principal\n"
        ]
        for text in texts:
            print(f"{text}")
    
    def pick_option(self):
        return input("Sélectionnez une option: ")
    
    def invalid_input(self, index, values):
        texts = {
            0: "Veuillez entrer le nombre indiqué pour la catégorie souhaitée.",
            1: "Le prénom ne peut contenir que des lettres et des tirets.",
            2: "Le nom ne peut contenir que des lettres et des tirets.",
            3: "La date de naissance n'est pas une date valide.",
            4: "Nos amis vampires, momies, squelettes ou autres zombies ne sont pas admis aux tournois de notre club.",
            5: "Les enfants en dessous de quatre ans ne sont pas admis aux tournois de notre club.",
            6: "L'ID est composé de 2 lettres suivies de 5 chiffres.",
            7: "Le nombre de joueurs doit être un nombre valide et être pair.",
            8: "Veuillez répondre 'o' / 'n' ou 'y' / 'n'.",
            9: "Le nom du tournoi ne peut pas être vide.",
            10: "La ville ne peut pas être vide.",
            11: "Le nombre de rounds doit être un nombre entier compris entre 1 et 20",
            12: "Les scores doivent être des nombres [0, 0.5, 1]."
        }
        message = texts.get(index, "Invalid index")
        print(message)
    
    def notify_alert(self, index, values):
        texts = {
            0: "Ajout impossible, cet ID existe déjà dans la base de données.",
            1: "Modification impossible, cet ID existe déjà dans la base de données.",
            2: "Joueur-euse ajouté avec succès.",
            3: "Aucun joueur enregistré avec cet ID.",
            4: "Joueur-euse modifié avec succès.",
            5: "Un tournoi est déjà en cours, cette action va l'écraser.",
            6: "Attention, générer un tournoi aléatoire va ajouter des joueurs aléatoires à votre BDD de joueurs.",
            7: f"Ajout du joueur {values[0]}/{values[1]}",
            8: f"Génération impossible, le fichier {values[0]} à été déplacé.",
            9: "Tournoi créé avec succès.",
            10: "Aucun nouveau tournoi / tournoi en cours n'a été trouvé, veuillez en créer un.",
            11: "Action impossible, aucun joueur enregistré.",
            12: "Action impossible, aucun tournoi n'a encore eu lieu.",
            13: "Action impossible, aucun round de ce tournoi n'est terminé.",
            14: "Action impossible, aucun match de ce tournoi n'a encore eu lieu.",
            15: "Fin de la liste des joueurs.",
            16: "Liste des joueurs exportée dans le dossier 'data/reports/'",
            17: f"{values[0]}\n{values[1]}",
            18: f"Round {values[0]} / {values[1]}",
            19: f"Match {values[0]} / {values[1]}",
            20: f"{values[0]} (pions noirs) vs {values[1]} (pions blancs)"
            
        }
        message = texts.get(index, "Invalid alert index")
        print(message)
    
    def user_prompts(self, index, values):
        prompts = {
            0: "Appuyez sur entrée pour revenir au menu précédent.",
            1: "ID : ",
            2: "Prénom : ",
            3: "Nom : ",
            4: "Date de naissance YYYY MM DD : ",
            5: "Êtes-vous sûr de vouloir faire cela ? ",
            6: "Combien de joueurs participent au tournoi : ",
            7: "Voulez-vous générer un tournoi aléatoire avec des joueurs aléatoires ? ",
            8: "Quelque chose à mal tourné, retour au menu précédent.",
            9: "Continuer ? ",
            10: "Nombre de tours : ",
            11: "Donnez une description du tournoi ou laisser vide : ",
            12: "Veuillez renseigner la ville ou se déroule le tournoi : ",
            13: "Veuillez renseigner le titre du tournoi : ",
            14: f"Page {values[0]}/{values[1]}                   page suivante >> ",
            15: f"Commencer le match {values[0]} (pions noirs) vs {values[1]} (pions blancs) ? ",
            16: f"Score de {values[0]} (0, 0.5, 1): ",
            17: "Prêts pour le prochain round ? ",
            18: "Voir les résultats du tournoi ?",
            19: "Fermer le tournoi et revenir au menu précédent ? "
        }
        prompt_message = prompts.get(index, "Invalid prompt index")
        user_input = input(prompt_message).strip()

        if index == 1:
            return user_input.upper()
        elif index in (2, 3, 13, 12):
            return user_input.title()
        else:
            return user_input
    
    def report_player_list(self, page_data):
        myTable = PrettyTable(["ID", "Prénom", "Nom", "Ddn"]) 
        for data in page_data:
            player_id = data.get("player_id", "N/A")
            first_name = data.get("first_name", "N/A")
            last_name = data.get("last_name", "N/A")
            birth_date = data.get("birth_date", "N/A")
            myTable.add_row([player_id, first_name, last_name, birth_date])
        
        print(myTable)
    
    def report_tournament_list(self, page_data):
        myTable = PrettyTable(["Titre", "Lieu", "Début", "Fin"]) 
        for data in page_data:
            tour_title = data['name']
            tour_city = data['city']
            tour_beg = data['start_date']
            tour_end = data['end_date']
            myTable.add_row([tour_title, tour_city, tour_beg, tour_end])
        print(myTable)
    
    def tournament_final_rank(self, tour_name, tour_city, tour_beg, tour_end, page_data):
        print(f"Résultats du {tour_name} in {tour_city}")
        print(f"Débuté le {tour_beg} et achevé le {tour_end}\n")
        myTable = PrettyTable(["ID", "Prénom", "Nom", "Score"]) 
        for data in page_data:
            player_id = data[0]
            first_name = data[1]
            last_name = data[2]
            birth_date = data[3]
            myTable.add_row([player_id, first_name, last_name, birth_date])
        
        print(myTable)
    
    def quit_message(self):
        MainView.clear_screen()
        self.menu_header(0)
        print("Merci d'avoir utilisé Chess Tournament Manager.")
        print("\nProgram quits elegantly.")
