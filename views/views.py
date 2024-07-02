import os
import time

class MainView:
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
            8: "Liste des joueurs\n",
            9: "Liste des tournois\n",
            10: "Nom, ville & date d'un tournoi\n",
            11: "Liste des joueurs d'un tournoi\n",
            12: "Liste de tous les matchs d'un tournoi\n"            
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
    
    def invalid_input(self, index):
        texts = {
            0: "Veuillez entrer le nombre indiqué pour la catégorie souhaitée.",
            1: "Le prénom ne peut contenir que des lettres et des tirets.",
            2: "Le nom ne peut contenir que des lettres et des tirets.",
            3: "La date de naissance n'est pas une date valide.",
            4: "Nos amis vampires, momies, squelettes ou autres zombies ne sont pas admis aux tournois de notre club.",
            5: "Les enfants en dessous de quatre ans ne sont pas admis aux tournois de notre club.",
            6: "L'ID est composé de 2 lettres suivies de 5 chiffres.",
            7: "Le nom du tournoi ne peut pas être vide.",
            8: "La ville ne peut pas être vide.",
            9: "Le nombre de rounds doit être un nombre pair entier.",
            10: "Les scores doivent être des nombres [0, 0.5, 1].",
            11: "Veuillez répondre 'o' / 'n' ou 'y' / 'n'."
        }
        message = texts.get(index, "Invalid index")
        print(message)
    
    def notify_alert(self, index):
        texts = {
            0: "Ajout impossible, cet ID existe déjà dans la base de données.",
            1: "Modification impossible, cet ID existe déjà dans la base de données.",
            2: "Un tournoi est déjà en cours, cette action va l'écraser.",
            3: "Attention, générer un tournoi aléatoire va ajouter des joueurs aléatoires à votre BDD de joueurs.",
            4: "Aucun nouveau tournoi / tournoi en cours n'a été trouvé, veuillez en créer un.",
            5: "Action impossible, aucun joueur enregistré.",
            6: "Action impossible, aucun tournoi n'a encore eu lieu.",
            7: "Action impossible, aucun round de ce tournoi n'est terminé.",
            8: "Action impossible, aucun match de ce tournoi n'a encore eu lieu.",
            9: "Joueur-euse ajouté avec succès.",
            10: "Tournoi créé avec succès."
        }
        message = texts.get(index, "Invalid alert index")
        print(message)
    
    def user_prompts(self, index):
        prompts = {
            0: "ID : ",
            1: "Prénom : ",
            2: "Nom : ",
            3: "Date de naissance YYYY MM DD : ",
            4: "Appuyez sur entrée pour revenir au menu précédent."
        }
        prompt_message = prompts.get(index, "Invalid prompt index")
        user_input = input(prompt_message).strip()

        if index == 0:
            return user_input.upper()
        elif index in (1, 2):
            return user_input.title()
        else:
            return user_input
    
    def confirm_action(self):
        print("\nÊtes-vous sûr de vouloir faire cela ?")
    
    def report_player_list(self, players_data):
        for data in players_data:
            print(f"ID [{data[0]}]  Prénom : {data[1]}  Nom : {data[2]}  Ddn : {data[3]}")
    
    def report_tournament_list(self, tournament_data):
        for data in tournament_data:
            print(f"Tournoi : {data[0]}  Ville : {data[1]}  Commencé le : {data[2]}  Terminé le : {data[3]}")
    
    def quit_message(self):
        MainView.clear_screen()
        self.menu_header(0)
        print("Merci d'avoir utilisé Chess Tournament Manager.")
        print("\nProgram quits elegantly.")
