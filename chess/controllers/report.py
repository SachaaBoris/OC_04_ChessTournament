from views.main import MainView
from models.player import PlayerDataManager
from prettytable import PrettyTable
from config_loader import EXPORT_TO_FILE, PLAYER_LIST_ORDER
from tinydb import TinyDB
import os


class ReportController:
    """Contrôleur de gestion des rapports"""

    def __init__(self):
        self.view = MainView()

    def report_menu(self):
        """Menu des rapports"""
        invalid_input = 0
        while True:
            if invalid_input == 0:
                self.view.clear_screen()
                self.view.display_menu("report")

            choice = self.view.user_prompts(21, ["", ""])

            if choice in ["1", "2", "3", "4", "5", "6"]:
                invalid_input = 0
                if choice == "1":
                    self.list_all_players()  # self.list_players()

                elif choice == "2":
                    self.list_all_tournaments()  # self.list_tournaments()

                elif choice == "3":
                    self.get_tournament_info("tour")  # self.get_tournament_info("tour")

                elif choice == "4":
                    self.get_tournament_info("players")  # self.get_tournament_info("players")

                elif choice == "5":
                    self.get_tournament_info("matches")  # self.get_tournament_info("matches")

                elif choice == "6":
                    break  # main menu

            else:
                # Invalid input
                invalid_input = 1
                self.view.invalid_input(0, ["", ""])

    def data_file_exists(self, file_name):
        """Returns bool"""
        if os.path.exists("data"):
            file_path = f'data/{file_name}.json'

        else:
            file_path = f'chess/data/{file_name}.json'

        if os.path.isfile(file_path):
            return True

        else:
            return False

    def transform_player_list(self, player_list):
        """Returns sorted dictionary"""
        transformed_list = []
        for player in player_list:
            player_dict = {
                'player_id': player[0],
                'first_name': player[1],
                'last_name': player[2],
                'birth_date': player[3]
            }
            transformed_list.append(player_dict)

        sorted_list = sorted(transformed_list, key=lambda x: x['last_name'])
        return sorted_list

    def list_all_players(self):
        """Lister tous les joueurs"""
        self.view.new_header(9)
        if self.data_file_exists("players"):
            players_list = PlayerDataManager().list_players(PLAYER_LIST_ORDER)
            total_players = len(players_list)

            if total_players > 20:
                self.report_player_pages(players_list)

            else:
                self.view.display_table("player_list", players_list)

            self.report_list_to_drive("1.full_players_list", players_list)
            self.view.notify_alert(15, ["", ""])
            self.view.user_prompts(0, ["", ""])

        else:
            self.view.new_header(9)
            self.view.notify_alert(11, ['data/players.json', ""])
            self.view.user_prompts(0, ["", ""])

    def report_list_to_drive(self, mode, file_data):
        """Enregistre le rapport dans le dossier data/reports"""
        if EXPORT_TO_FILE:
            file_name = mode
            if os.path.exists("data"):
                report_path = f'data/reports/{file_name}.txt'
            else:
                report_path = f'chess/data/reports/{file_name}.txt'

            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            my_tables = []
            full_report = ""

            if mode == "1.full_players_list":
                table_data = self.view.get_table_player("pick_player", file_data)
                string = "Liste des joueurs exportée"
                my_table = PrettyTable(["Index", "ID", "Prénom", "Nom", "Ddn"])
                for data in table_data:
                    my_table.add_row(data[:len(data)])
                my_tables.append(my_table)

            elif mode == "2.full_tournaments_list":
                table_data = self.view.get_table_tournament("pick_tournament", file_data)
                string = "Liste des tournois exportée"
                my_table = PrettyTable(["Index", "Nom", "Lieu", "Début", "Fin"])
                for data in table_data:
                    my_table.add_row(data[:len(data)])
                my_tables.append(my_table)

            elif mode == "3.single_tournament_info":
                table_data = self.view.get_table_tournament("tournament_info", file_data[0], file_data[1])
                string = "Informations du tournoi exporté"
                my_table = PrettyTable(["Titre", "Lieu", "Joueurs", "Tours", "Début", "Fin", "Gagnant.e"])
                for data in table_data:
                    my_table.add_row(data[:len(data)])
                my_tables.append(my_table)

            elif mode == "4.tournament_players":
                string = "Liste des joueurs du tournoi exportée"
                players_list = file_data[0][0].get('players')
                players_dict = [{
                    'player_id': player[0],
                    'first_name': player[1],
                    'last_name': player[2],
                    'birth_date': player[3]
                    } for player in players_list]
                player_points = file_data[3]
                table_data = self.view.get_table_player("player_scores", players_dict, player_points)
                tournament_name = file_data[0][0].get('tournament_name')
                tournament_location = file_data[0][0].get('city')
                full_report += f"Nom du tournoi : {tournament_name}\nLieu : {tournament_location}\n\n"
                string = "Liste des joueurs du tournoi exportée"
                my_table = PrettyTable(["ID", "Prénom", "Nom", "Ddn", "Points"])
                for data in table_data:
                    my_table.add_row(data[:len(data)])

                full_report += my_table.get_string() + "\n\n"

            elif mode == "5.tournament_review":
                tournament_data, winner, round_results, final_results = file_data
                string = "Revue du tournoi exportée"
                tournament_name = tournament_data[0].get('tournament_name')
                tournament_location = tournament_data[0].get('city')
                full_report += f"Nom du tournoi : {tournament_name}\nLieu : {tournament_location}\n\n"
                for i, round_result in enumerate(round_results):
                    round_table_data = self.view.get_table_match("match_list", round_result[1])
                    round_table = PrettyTable([
                        "Début",
                        "Joueur 1",
                        "Score J1",
                        "Score J2",
                        "Joueur 2",
                        "Fin",
                        "Durée"
                        ])
                    for row in round_table_data:
                        round_table.add_row(row)

                    full_report += f"Résultats du round {i + 1}/{len(round_results)} :\n"
                    full_report += round_table.get_string() + "\n\n"

                if len(final_results) > 0:
                    final_table_data = self.view.get_table_rank(final_results)
                    final_table = PrettyTable(["ID", "Prénom", "Nom", "Score"])
                    for row in final_table_data:
                        final_table.add_row(row)

                    full_report += "Résultats du tournoi :\n"
                    full_report += final_table.get_string() + "\n\n"

            if mode not in ["4.tournament_players", "5.tournament_review"]:
                header_text = string.rsplit(' ', 1)[0]
                full_report = header_text + "\n\n"
                for table in my_tables:
                    full_report += table.get_string() + "\n\n"

            else:
                header_text = string.rsplit(' ', 1)[0]
                full_report = header_text + "\n\n" + full_report

            with open(report_path, 'w') as report_file:
                report_file.write(full_report)
                self.view.notify_alert(16, [string, ""])

    def get_players_points(self, tournament_results):
        """Returns player_scores dict"""
        player_scores = {}

        for round_result in tournament_results:
            matches = round_result[1]

            for match in matches:
                _, players, scores = match
                p1_id, p2_id = players[0][0], players[1][0]
                score_p1, score_p2 = scores

                if p1_id not in player_scores:
                    player_scores[p1_id] = 0.0
                if p2_id not in player_scores:
                    player_scores[p2_id] = 0.0

                player_scores[p1_id] += score_p1
                player_scores[p2_id] += score_p2

        return player_scores

    def get_tournament_winner(self, tournament):
        """Returns winner's name"""
        end_date = tournament[0]['end_date']
        if end_date != "":
            final_results = tournament[0]['final_results']
            if final_results:
                winner_data = final_results[0]
                winner_name = f"{winner_data[1]} {winner_data[2]}"
                return winner_name
        else:
            # Le tournoi n'est pas terminé
            return "..."

    def report_player_pages(self, players_list, player_points=None):
        """Créé des pages pour l'affichage des tableaux de joueurs"""
        page_size = 20
        total_players = len(players_list)
        total_pages = (total_players // page_size) + (1 if total_players % page_size != 0 else 0)

        for page in range(total_pages):
            self.view.new_header(9)
            start_index = page * page_size
            end_index = start_index + page_size
            page_data = players_list[start_index:end_index]
            if player_points is None:
                self.view.display_table("player_list", page_data)
            else:
                self.view.display_table("player_scores", page_data, player_points)

            if page < total_pages - 1:
                self.view.user_prompts(14, [page + 1, total_pages])

    def report_rounds_pages(self, round_results, tour_info):
        """Créé des pages pour l'affichage des tableaux de rounds"""
        total_pages = len(round_results)
        for page in range(total_pages):
            self.view.new_header(13)
            self.view.notify_alert(22, [tour_info[0], tour_info[1]])
            self.view.notify_alert(23, [page + 1, ""])
            self.view.display_table("match_list", round_results[page][1])

            if page < total_pages - 1:
                self.view.user_prompts(14, [page + 1, total_pages])

    def get_tournament_data(self, path):
        """Returns tournament_data dictionnary"""
        db = TinyDB(path)
        tournaments_table = db.table('tournaments')
        tournaments = tournaments_table.all()
        db.close()

        return tournaments

    def list_tournaments(self, status):
        """Returns list of tournaments"""
        if os.path.exists("data"):
            relative_path = 'data/'
        else:
            relative_path = 'chess/data/'

        tournaments_path = f"{relative_path}tournaments.json"
        tournaments = []

        if os.path.exists(tournaments_path):
            tournaments = self.get_tournament_data(tournaments_path)

            if status == "pending":
                tournaments = [tournament for tournament in tournaments if tournament.get('beg_date') != ""]

            elif status == "ended":
                tournaments = [tournament for tournament in tournaments if tournament.get('end_date') != ""]

            elif status == "created":
                tournaments = [tournament for tournament in tournaments if tournament.get('beg_date') == ""]

        return tournaments

    def list_all_tournaments(self):
        """Lister les tournois"""
        tournaments = self.list_tournaments("all")
        n_tour = len(tournaments)
        if n_tour > 0:
            self.view.new_header(10)
            self.view.display_table("tournament_list", tournaments)
            self.report_list_to_drive("2.full_tournaments_list", tournaments)

        else:
            self.view.notify_alert(21, ["", ""])

        self.view.user_prompts(0, ["", ""])

    def get_tournament_info(self, mode):
        """Extraire les data d'un tournoi"""
        if mode == "matches":
            tournaments = self.list_tournaments("pending")

        else:
            tournaments = self.list_tournaments("all")

        n_tour = len(tournaments)
        if n_tour > 0:
            self.view.new_header(10)
            self.view.display_table("pick_tournament", tournaments)

            while True:
                choice = self.view.user_prompts(20, ["", ""])
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= n_tour:
                        choice = choice - 1
                        tournament_data = [tournaments[choice]]
                        winner = self.get_tournament_winner(tournament_data)

                        if mode == "tour":
                            self.view.new_header(11)
                            self.view.display_table("tournament_info", tournament_data, winner)
                            tour_data = [tournament_data, winner]
                            self.report_list_to_drive("3.single_tournament_info", tour_data)

                        elif mode == "players":
                            self.view.new_header(12)
                            for data in tournament_data:
                                players_list = data['players']

                            players_list = self.transform_player_list(players_list)  # list to dict
                            total_players = len(players_list)
                            tournament_results = tournament_data[0].get('rounds_results')
                            player_points = self.get_players_points(tournament_results)

                            if total_players > 20:
                                self.report_player_pages(players_list, player_points)

                            else:
                                self.view.display_table("player_scores", players_list, player_points)

                            tour_data = [tournament_data, winner, players_list, player_points]
                            self.report_list_to_drive("4.tournament_players", tour_data)

                        elif mode == "matches":
                            self.view.new_header(13)
                            for data in tournament_data:
                                round_results = data['rounds_results']

                            tour_info = [tournament_data[0].get('tournament_name'), tournament_data[0].get('city')]
                            self.report_rounds_pages(round_results, tour_info)
                            final_results = tournament_data[0].get('final_results')
                            if len(final_results) > 0:
                                self.view.user_prompts(18, ["", ""])
                                self.view.new_header(13)
                                tour_beg = tournament_data[0].get('beg_date')
                                tour_end = tournament_data[0].get('end_date')
                                self.view.display_table(
                                    "tournament_final_rank",
                                    final_results,
                                    additional_info=(
                                        tour_info[0], tour_info[1],
                                        tour_beg, tour_end)
                                )
                            tour_data = [tournament_data, winner, round_results, final_results]
                            self.report_list_to_drive("5.tournament_review", tour_data)

                        break

                    else:
                        self.view.invalid_input(13, ["", ""])

                else:
                    if choice == "q":
                        return

                    self.view.invalid_input(13, ["", ""])

        else:
            self.view.notify_alert(21, ["", ""])

        self.view.user_prompts(0, ["", ""])
