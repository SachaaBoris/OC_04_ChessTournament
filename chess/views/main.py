import os
from prettytable import PrettyTable
from datetime import datetime


class MainView:
    """ vue principale """

    def clear_screen(self):
        """ reset l'affichage """
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_header(self, index):
        """ affiche un header """
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
        print("Chess Tournament Manager v0.1\n" + f"{message}")

    def new_header(self, index):
        self.clear_screen()
        self.menu_header(index)

    def display_menu(self, type):
        """ affiche le menu du type voulu """

        if type == "main":  # affiche le menu principal
            self.menu_header(1)
            texts = [
                "1 - Gestion des joueurs",
                "2 - Gestion des tournois",
                "3 - Générer des rapports",
                "4 - Quitter\n"
            ]

        if type == "player":  # affiche le menu de gestion des joueurs
            self.menu_header(2)
            texts = [
                "1 - Ajouter un joueur",
                "2 - Modifier un joueur",
                "3 - Voir la liste des joueurs",
                "4 - Revenir au menu principal\n"
            ]

        if type == "tournament":  # affiche le menu de gestion des tournois
            self.menu_header(3)
            texts = [
                "1 - Préparer un tournoi",
                "2 - Lancer / Reprendre un tournoi",
                "3 - Voir la liste des tournois",
                "4 - Revenir au menu principal\n"
            ]

        if type == "report":  # affiche le menu des rapports
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

    def invalid_input(self, index, values):
        """ affiche une alerte """
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
            12: "Les scores doivent être des nombres [0, 0.5, 1].",
            13: "Veuillez entrer l'ID du tournoi souhaité.",
            14: "Veuillez entrer l'ID du match souhaité.",
            15: "Veuillez entrer l'index du résultat.",
            16: f"Veuillez entrer l'index du joueur souhaité ([{values[0]}]-[{values[1]}])"
        }
        message = texts.get(index, "Invalid index")
        print(message)

    def notify_alert(self, index, values):
        """ affiche une notification """
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
            20: f"{values[0]} vs {values[1]}",
            21: "Aucun tournoi n'a été trouvé.",
            22: f"{values[0]}, ayant eu lieu a {values[1]}",
            23: f"Round {values[0]} : ",
            24: f"Titre : {values[0]}\nVille : {values[1]}",
            25: f"Page : {values[0]} / {values[1]}",
            26: "Action impossible, ce joueur est déjà enregistré dans le tournoi.",
            27: f"Joueurs participants au nouveau tournoi : {values[0]} / {values[1]} ",
            28: "(laissez vide pour passer)",
            29: "Aucun joueur n'a été modifié.",
            30: f"Joueur à modifier : {values[0]} {values[1]}",
            31: "Erreur de decodage Json.",
            32: "L'attribut 'players' n'existe pas dans le dictionnaire."
        }
        message = texts.get(index, "Invalid alert index")
        print(message)

    def user_prompts(self, index, values):
        """ affiche les prompts utilisateurs """
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
            10: "Nombre de tours (laisser vide pour 4 tours) : ",
            11: "Donnez une description du tournoi ou laisser vide : ",
            12: "Veuillez renseigner la ville ou se déroule le tournoi : ",
            13: "Veuillez renseigner le titre du tournoi : ",
            14: f"Page {values[0]}/{values[1]}                   page suivante >> ",
            15: f"Commencer le match {values[0]} vs {values[1]} ? ",
            16: f"Score de {values[0]} (0, 0.5, 1): ",
            17: "Prêts pour le prochain round ? ",
            18: "Voir les résultats du tournoi ?",
            19: "Fermer le tournoi et revenir au menu précédent ? ",
            20: "Veuillez selectionner un tournoi : ",
            21: "Sélectionnez une option: ",
            22: "Voulez-vous donner des scores aléatoires aux matchs de ce round ? ",
            23: f"{values[0]} {values[1]}",
            24: "Quel match voulez-vous mettre à jour : ",
            25: f"[0] match nul, [1] {values[0]} a gagné, [2] {values[1]} a gagné : ",
            26: "Voulez-vous ajouter des joueurs de la BDD ? ",
            27: f"Choisissez un index ([1]-[{values[0]}]) de joueur à {values[1]}\nou laissez vide pour passer : "
        }
        prompt_message = prompts.get(index, "Invalid prompt index")
        user_input = input(prompt_message).strip()

        if index == 1:
            return user_input.upper()
        elif index in (2, 3, 13, 12):
            return user_input.title()
        else:
            return user_input

    def quit_message(self):
        """ affiche un message d'adieu """
        MainView().clear_screen()
        self.menu_header(0)
        print("Merci d'avoir utilisé Chess Tournament Manager.")
        print("\nProgram quits elegantly.")

    def display_table(self, table_type, page_data, additional_info=None):
        """ affiche une table basée sur le type fourni """

        if table_type in ["round_matches", "match_list"]:
            if table_type == "round_matches":
                my_table = PrettyTable(["ID", "Joueur 1", "Score J1", "Score J2", "Joueur 2", "Durée"])
            else:
                my_table = PrettyTable(["Début", "Joueur 1", "Score J1", "Score J2", "Joueur 2", "Fin", "Durée"])

            for index, data in enumerate(page_data):
                match_id = index + 1
                match_p1 = f"{data[1][0][1]} {data[1][0][2]}"
                p1_score = data[2][0] if data[2][0] != -1 else ""
                p2_score = data[2][1] if data[2][1] != -1 else ""
                match_p2 = f"{data[1][1][1]} {data[1][1][2]}"
                beg_date = data[0][0]
                end_date = data[0][1]

                if end_date != "":
                    start_datetime = datetime.strptime(beg_date, "%Y-%m-%d_%H:%M")
                    end_datetime = datetime.strptime(end_date, "%Y-%m-%d_%H:%M")
                    duration_calc = end_datetime - start_datetime
                    hours, remainder = divmod(duration_calc.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)
                    duration = f"{int(hours):02}:{int(minutes):02}"
                    beg_date = f"{beg_date.split('_')[1]}"
                    end_date = f"{end_date.split('_')[1]}"
                else:
                    if beg_date == "":
                        beg_date = "X"
                        end_date = "X"
                        duration = "X" if table_type == "match_list" else "Start match ?"
                    else:
                        beg_date = f"Started @ {beg_date.split('_')[1]}"
                        duration = "X" if table_type == "match_list" else beg_date

                if table_type == "match_list":
                    my_table.add_row([beg_date, match_p1, p1_score, p2_score, match_p2, end_date, duration])
                else:
                    my_table.add_row([match_id, match_p1, p1_score, p2_score, match_p2, duration])

        elif table_type in ["player_list", "pick_player"]:
            if table_type == "player_list":
                my_table = PrettyTable(["ID", "Prénom", "Nom", "Ddn"])
            else:
                my_table = PrettyTable(["Index", "ID", "Prénom", "Nom", "Ddn"])

            for index, data in enumerate(page_data):
                player_index = index + 1
                player_id = data.get("player_id", "N/A")
                first_name = data.get("first_name", "N/A")
                last_name = data.get("last_name", "N/A")
                birth_date = data.get("birth_date", "N/A")
                if table_type == "pick_player":
                    my_table.add_row([player_index, player_id, first_name, last_name, birth_date])
                else:
                    my_table.add_row([player_id, first_name, last_name, birth_date])

        elif table_type in ["tournament_list", "pick_tournament"]:
            if table_type == "tournament_list":
                my_table = PrettyTable(["Titre", "Lieu", "Début", "Fin"])
            else:
                my_table = PrettyTable(["ID", "Titre", "Lieu", "Début", "Fin"])

            for index, data in enumerate(page_data):
                tour_id = index + 1
                tour_title = data['tournament_name']
                tour_city = data['city']
                tour_beg = "Non débuté..." if data['beg_date'] == "" else data['beg_date']
                tour_end = "Non débuté..." if tour_beg == "Non débuté..." else (
                    "En cours..." if data['end_date'] == "" else data['end_date'])
                if table_type == "pick_tournament":
                    my_table.add_row([tour_id, tour_title, tour_city, tour_beg, tour_end])
                else:
                    my_table.add_row([tour_title, tour_city, tour_beg, tour_end])

        elif table_type == "tournament_final_rank":
            tour_name, tour_city, tour_beg, tour_end = additional_info
            print(f"Résultats du {tour_name} in {tour_city}")
            print(f"Débuté le {tour_beg} et achevé le {tour_end}\n")
            my_table = PrettyTable(["ID", "Prénom", "Nom", "Score"])
            for data in page_data:
                player_id = data[0]
                first_name = data[1]
                last_name = data[2]
                score = data[3]
                my_table.add_row([player_id, first_name, last_name, score])

        print(my_table)
