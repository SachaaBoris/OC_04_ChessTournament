import os
from prettytable import PrettyTable
from datetime import datetime


class MainView:
    """Vue principale"""

    def clear_screen(self):
        """Reset l'affichage"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_header(self, index):
        """Affiche un header"""
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
            11: "Informations d'un tournoi\n",
            12: "Liste des joueurs d'un tournoi\n",
            13: "Liste de tous les matchs d'un tournoi\n",
            14: "Scores finaux du tournoi\n"
        }
        message = texts.get(index, "Invalid header index")
        print("Chess Tournament Manager v0.1" + "\n" + f"{message}")

    def new_header(self, index):
        """Refresh menu header"""
        self.clear_screen()
        self.menu_header(index)

    def display_menu(self, type):
        """Affiche le menu du type voulu"""

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
                "3 - Informations d'un tournoi spécifique",
                "4 - Lister tous les joueurs d'un tournoi spécifique",
                "5 - Lister tous les matchs de tous les tours d'un tournoi spécifique",
                "6 - Revenir au menu principal\n"
            ]

        for text in texts:
            print(f"{text}")

    def invalid_input(self, index, values):
        """Affiche une alerte"""
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
        print('\033[93m'+message+'\033[96m')

    def notify_alert(self, index, values):
        """Affiche une notification"""
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
            16: f"{values[0]} dans le dossier 'data/reports/'",
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
            27: f"Joueurs selectionés : {values[0]} / {values[1]} ",
            28: "(laissez vide pour garder les anciennes données)",
            29: "Le joueur n'a pas été modifié.",
            30: f"Joueur à modifier : {values[0]} {values[1]}",
            31: "Erreur de decodage Json.",
            32: "L'attribut 'players' n'existe pas dans le dictionnaire.",
            33: "Remplacer les scores d'un match déjà terminé."
        }
        message = texts.get(index, "Invalid alert index")
        print(message)

    def user_prompts(self, index, values):
        """Affiche un prompt utilisateur"""
        prompts = {
            0: "Entrée pour revenir au menu précédent.",
            1: "ID : ",
            2: "Prénom : ",
            3: "Nom : ",
            4: "Date de naissance (dd mm yyyy) : ",
            5: "Êtes-vous sûr ? ",
            6: "Combien de joueurs participent au tournoi : ",
            7: "Générer un tournoi aléatoire avec des joueurs aléatoires ? ",
            8: "Quelque chose à mal tourné, retour au menu précédent.",
            9: "Entrée pour continuer : ",
            10: "Nombre de tours (laisser vide pour 4 tours) : ",
            11: "Donnez une description du tournoi ou laisser vide : ",
            12: "Renseigner la ville ou se déroule le tournoi : ",
            13: "Renseigner le titre du tournoi : ",
            14: f"Page {values[0]}/{values[1]}                   page suivante >> ",
            15: f"Commencer le match {values[0]} vs {values[1]} ? ",
            16: f"Score de {values[0]} (0, 0.5, 1): ",
            17: "Entrée pour lancer le prochain round / [q] pour quitter : ",
            18: "Entrée pour voir les résultats du tournoi :",
            19: "Entrée pour revenir au menu précédent : ",
            20: "Veuillez selectionner un tournoi ([q] pour quitter) : ",
            21: "Sélectionnez une option: ",
            22: "Voulez-vous donner des scores aléatoires aux matchs de ce round ? ",
            23: f"{values[0]} {values[1]}",
            24: "Quel match voulez-vous commencer / terminer ([q] pour quitter) : ",
            25: f"[0] match nul, [1] {values[0]} a gagné, [2] {values[1]} a gagné : ",
            26: "Voulez-vous ajouter des joueurs de la BDD ? ",
            27: (f"Choisissez un index ([1]-[{values[0]}\n"
                 f"ou laissez vide pour {values[1]} : ")
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
        """Affiche un message d'adieu"""
        MainView().clear_screen()
        self.menu_header(0)
        print("Merci d'avoir utilisé Chess Tournament Manager.")
        print("\nProgram quits elegantly."+'\033[0m')

    def display_table(self, table_type, page_data, additional_info=None):
        """Affiche une table basée sur le type fourni"""
        if table_type in ["round_matches", "match_list"]:
            table_data = self.get_table_match(table_type, page_data)
            if table_type == "round_matches":
                my_table = PrettyTable(["ID", "Joueur 1", "Score J1", "Score J2", "Joueur 2", "Durée"])
            else:  # "match_list"
                my_table = PrettyTable(["Début", "Joueur 1", "Score J1", "Score J2", "Joueur 2", "Fin", "Durée"])

        elif table_type in ["player_list", "pick_player", "player_scores"]:
            table_data = self.get_table_player(table_type, page_data, additional_info)
            if table_type == "player_list":
                my_table = PrettyTable(["ID", "Prénom", "Nom", "Ddn"])
            elif table_type == "pick_player":
                my_table = PrettyTable(["Index", "ID", "Prénom", "Nom", "Ddn"])
            else:  # "player_scores"
                my_table = PrettyTable(["ID", "Prénom", "Nom", "Ddn", "Points"])

        elif table_type in ["tournament_list", "pick_tournament", "tournament_info"]:
            table_data = self.get_table_tournament(table_type, page_data, additional_info)
            if table_type == "tournament_list":
                my_table = PrettyTable(["Titre", "Lieu", "Début", "Fin"])
            elif table_type == "pick_tournament":
                my_table = PrettyTable(["ID", "Titre", "Lieu", "Début", "Fin"])
            else:  # "tournament_info"
                my_table = PrettyTable(["Titre", "Lieu", "Joueurs", "Tours", "Début", "Fin", "Gagnant.e"])

        elif table_type == "tournament_final_rank":
            table_data = self.get_table_rank(page_data)
            tour_name, tour_city, tour_beg, tour_end = additional_info
            print(f"Résultats du {tour_name} in {tour_city}")
            print(f"Débuté le {tour_beg} et achevé le {tour_end}\n")
            my_table = PrettyTable(["ID", "Prénom", "Nom", "Points"])

        for data in table_data:
            my_table.add_row(data[:len(data)])

        table_width = self.calculate_table_width(my_table)
        if table_width > 130:
            cmd = f"mode {table_width + 2},35"
            os.system(cmd)
            header_index = self.get_new_header(table_type)
            self.new_header(header_index)
        print(my_table)

    def get_new_header(self, table_type):
        """Détermine le header de la page"""
        if table_type in ["round_matches", "match_list"]:
            if table_type == "round_matches":
                index = 8
            else:  # "match_list"
                index = 13

        elif table_type in ["player_list", "pick_player", "player_scores"]:
            index = 9

        elif table_type in ["tournament_list", "pick_tournament"]:
            index = 10

        elif table_type == "tournament_info":
            index = 11

        elif table_type == "tournament_final_rank":
            index = 14

        return index

    def calculate_table_width(self, table):
        """Returns table width"""
        table_str = table.get_string()
        first_line = table_str.split('\n')[0]
        return len(first_line)

    def get_table_player(self, table_type, page_data, players_points=None):
        """Returns players table to print"""
        table_data = []
        for index, data in enumerate(page_data):
            player_index = index + 1
            player_id = data.get("player_id", "N/A")
            first_name = data.get("first_name", "N/A")
            last_name = data.get("last_name", "N/A")
            birth_date = data.get("birth_date", "N/A")
            if table_type == "pick_player":
                table_data.append([player_index, player_id, first_name, last_name, birth_date])
            elif table_type == "player_list":
                table_data.append([player_id, first_name, last_name, birth_date])
            else:  # "player_scores"
                points = players_points.get(player_id)
                table_data.append([player_id, first_name, last_name, birth_date, points])

        return table_data

    def get_table_tournament(self, table_type, page_data, additional_info=None):
        """Returns tournaments table to print"""
        table_data = []
        for index, data in enumerate(page_data):
            tour_id = index + 1
            tour_title = data['tournament_name']
            tour_city = data['city']
            tour_players = len(data['players'])
            tour_tours = data['rounds']
            tour_beg = "Non débuté..." if data['beg_date'] == "" else data['beg_date']
            tour_end = "Non débuté..." if tour_beg == "Non débuté..." else (
                "En cours..." if data['end_date'] == "" else data['end_date'])
            if table_type == "tournament_list":
                table_data.append([tour_title, tour_city, tour_beg, tour_end])
            elif table_type == "pick_tournament":
                table_data.append([tour_id, tour_title, tour_city, tour_beg, tour_end])
            else:  # table_type == "tournament_info"
                winner = additional_info
                table_data.append([
                    tour_title, tour_city, tour_players,
                    tour_tours, tour_beg, tour_end, winner])
                return table_data

        return table_data

    def get_table_match(self, table_type, page_data):
        """Returns match table to print"""
        table_data = []
        for index, data in enumerate(page_data):
            match_id = index + 1
            match_p1 = f"{data[1][0][1]} {data[1][0][2]}"
            p1_score = data[2][0] if data[2][0] != -1 else ""
            p2_score = data[2][1] if data[2][1] != -1 else ""
            match_p2 = f"{data[1][1][1]} {data[1][1][2]}"
            beg_date = data[0][0]
            end_date = data[0][1]
            beg_date, end_date, duration = self.get_duration(table_type, beg_date, end_date)

            if table_type == "match_list":
                table_data.append([beg_date, match_p1, p1_score, p2_score, match_p2, end_date, duration])
            else:
                table_data.append([match_id, match_p1, p1_score, p2_score, match_p2, duration])

        return table_data

    def get_duration(self, table_type, beg_date, end_date):
        """Returns beg_date, end_date, duration"""
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

        return beg_date, end_date, duration

    def get_table_rank(self, page_data):
        """Returns rank table to print"""
        table_data = []
        for data in page_data:
            player_id = data[0]
            first_name = data[1]
            last_name = data[2]
            score = data[3]
            table_data.append([player_id, first_name, last_name, score])

        return table_data
