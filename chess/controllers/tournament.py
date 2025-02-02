from views.main import MainView
from controllers.player import PlayerController
from controllers.report import ReportController
from models.player import PlayerDataManager
from models.tournament import TournamentDataManager
from config_loader import AUTOMATIC_FILL
from datetime import datetime, timedelta
import random
import json
import os


class TournamentController:
    """Contrôleur de gestion des tournois"""

    def __init__(self):
        self.view = MainView()

    def tournament_menu(self):
        """Menu de gestion des tournois"""
        invalid_input = 0
        while True:
            if invalid_input == 0:
                self.view.clear_screen()
                self.view.display_menu("tournament")

            choice = self.view.user_prompts(21, ["", ""])

            if choice in ["1", "2", "3", "4"]:
                invalid_input = 0
                if choice == "1":
                    self.create_tournament()  # self.create_tournament()

                elif choice == "2":
                    self.can_resume_tournament()  # self.can_resume_tournament()

                elif choice == "3":
                    ReportController().list_all_tournaments()  # ReportController().list_tournaments()

                elif choice == "4":
                    break  # main menu

            else:
                # Invalid input
                invalid_input = 1
                self.view.invalid_input(0, ["", ""])

    def data_file_exists(self, file_name):
        """Returns [bool, path]"""
        if os.path.exists("data"):
            file_path = f'data/{file_name}.json'

        else:
            file_path = f'chess/data/{file_name}.json'

        if os.path.isfile(file_path):
            return [True, file_path]

        else:
            return [False, '']

    def user_confirm(self, index):
        while True:
            choice = self.view.user_prompts(index, ["", ""]).lower()
            if choice in ["y", "yes", "o", "oui"]:
                return True
            else:
                if choice in ["n", "no", "non"]:
                    return False
                else:
                    self.view.invalid_input(8, ["", ""])

    def generate_random_tour_title_city(self):
        """Returns [str(tour_name), str(tour_city)]"""
        file_path = self.data_file_exists("randomizer")
        if file_path[0]:
            with open(file_path[1], 'r', encoding='utf-8') as file:
                random_data = json.load(file)
                tour_titles = random_data.get('tour_titles', None)
                tour_cities = random_data.get('cities', None)

            tour_city = random.choice(tour_cities)
            tour_title0 = tour_city.split(",")[0].strip()
            tour_title1 = random.choice(tour_titles[0])
            tour_title2 = random.choice(tour_titles[1])
            year_now = datetime.today().strftime("%Y")
            a = random.choice([1, 2, 3, 4, 5, 6])
            if a == 1:
                tour_name = f"{tour_title1} Chess {tour_title2}"

            elif a == 2:
                tour_name = f"{tour_title1} Chess {tour_title2} {year_now[2:]}"

            elif a == 3:
                tour_name = f"{tour_title1} {tour_title2} {year_now[2:]}"

            elif a == 4:
                tour_name = f"{tour_title0} Chess {tour_title2} {year_now[2:]}"

            elif a == 5:
                tour_name = f"The {tour_title0} {tour_title1} {tour_title2}"

            else:
                tour_name = f"{tour_title1} {tour_title2}"

            return [tour_name, tour_city]

        return ["", ""]

    def create_tournament(self):
        """Menu de creation de tournoi"""
        self.view.new_header(8)
        new_tournament = self.get_tournament_details()
        tournament = TournamentDataManager().initialize_tournament_list(new_tournament)
        TournamentDataManager().save_new_tournament(tournament)
        self.view.notify_alert(24, [tournament.tournament_name, tournament.city])
        self.view.notify_alert(9, ["", ""])
        self.view.user_prompts(0, ["", ""])

    def get_tournament_details(self):
        """Returns Tournament"""
        number_of_players = self.get_tournement_how_many_players()
        if AUTOMATIC_FILL:
            tour_players = self.get_tournament_automatic(number_of_players)
            tour_desc = ""
            title_city = self.generate_random_tour_title_city()
            tour_city = title_city[1]
            tour_title = title_city[0]

        else:
            tour_players = []

        tour_rounds = self.get_tournament_rounds()

        if len(tour_players) == 0:
            bdd_players = False
            file_path = self.data_file_exists("players")
            if file_path[0]:
                bdd_players = self.user_confirm(26)

            if bdd_players:
                tour_players = PlayerController().pick_a_player("tournament", number_of_players)
                self.view.new_header(7)

            for n in range(number_of_players - len(tour_players)):
                self.view.notify_alert(7, [len(tour_players), number_of_players])
                new_player = list([PlayerController().get_player_details("tournament")][0])
                tour_players.append(new_player)

            tour_desc = self.view.user_prompts(11, ["", ""])
            tour_city = self.view.user_prompts(12, ["", ""])
            tour_title = self.view.user_prompts(13, ["", ""])

        new_tournament = []
        if len(tour_players) > 0:
            PlayerDataManager().save_player_list(tour_players)

            # initialisation de valeures vides
            tour_round = 0
            tour_rounds_results = []
            tour_final_results = []
            tour_beg_date = ""
            tour_end_date = ""

            new_tournament = [
                tour_title,
                tour_city,
                tour_desc,
                tour_players,
                tour_rounds,
                tour_round,
                tour_rounds_results,
                tour_final_results,
                tour_beg_date,
                tour_end_date
            ]

        return new_tournament

    def get_tournement_how_many_players(self):
        """Returns int number_of_players"""
        while True:
            try:
                number_of_players = int(self.view.user_prompts(6, ["", ""]))
                if 2 <= number_of_players <= 98:
                    break

                else:
                    self.view.invalid_input(7, ["", ""])

            except ValueError:
                self.view.invalid_input(7, ["", ""])

        return number_of_players

    def get_tournament_automatic(self, number_of_players):
        """Returns list of tournament players"""
        tour_players = []
        while True:
            # ajouter des joueurs aleatoires ? (debug func)
            automatic = self.user_confirm(7)
            if automatic:
                self.view.notify_alert(6, ["", ""])
                sure = self.user_confirm(5)
                if sure:
                    tour_players = PlayerController().generate_random_players(number_of_players)
                    break

                else:
                    break

            else:
                break

        return tour_players

    def get_tournament_rounds(self):
        """Returns int(tour_rounds)"""
        while True:
            tour_rounds = self.view.user_prompts(10, ["", ""])
            if tour_rounds in ["0", ""]:
                tour_rounds = "4"

            try:
                tour_rounds = int(tour_rounds)
                if 1 <= tour_rounds <= 99:
                    break

                else:
                    self.view.invalid_input(11, ["", ""])

            except ValueError:
                self.view.invalid_input(11, ["", ""])

        return tour_rounds

    def can_resume_tournament(self):
        """Verifie le statut de pending_tournament"""
        self.view.new_header(8)
        file_path = self.data_file_exists("tournaments")

        if file_path[0]:
            tournaments = TournamentDataManager().list_tournaments()
            pending_tournaments = [data for data in tournaments if data['end_date'] == ""]

            if pending_tournaments:
                self.pick_tournament(pending_tournaments)

            else:
                self.view.notify_alert(10, ["", ""])
                self.view.user_prompts(0, ["", ""])

        else:
            self.view.notify_alert(10, ["", ""])
            self.view.user_prompts(0, ["", ""])

    def pick_tournament(self, pending_tournaments):
        """Choisir un tournoi à reprendre"""
        self.view.new_header(8)
        self.view.display_table("pick_tournament", pending_tournaments)

        while True:
            choice = self.view.user_prompts(20, ["", ""])
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(pending_tournaments):
                    selected_tournament = pending_tournaments[choice - 1]
                    self.tournament_status(selected_tournament)
                    break

                else:
                    self.view.invalid_input(13, ["", ""])

            else:
                if choice == "q":
                    break

                else:
                    self.view.invalid_input(13, ["", ""])

    def tournament_status(self, selected_tournament):
        """Détermine quel methode appliquer pour la reprise du tournoi"""
        tournament = TournamentDataManager().initialize_tournament_dict(selected_tournament)

        if selected_tournament.get('beg_date') == "":
            self.start_tournament(tournament)

        else:
            self.resume_tournament(tournament)

    def start_tournament(self, tournament):
        """Démarre le tournoi"""
        tour_round = 1
        tour_rounds_results = self.prepare_first_round(tournament.players)
        tour_beg_date = datetime.now().strftime('%Y-%m-%d_%H:%M')
        tournament.round = tour_round
        tournament.rounds_results = tour_rounds_results
        tournament.beg_date = tour_beg_date
        TournamentDataManager().update_tournament(tournament)
        self.resume_tournament(tournament)

    def prepare_first_round(self, players):
        """Returns list [first_round]"""
        random.shuffle(players)
        round = []

        for i in range(0, len(players), 2):
            round.append([["", ""], [players[i], players[i+1]], [-1, -1]])

        return [["Round 1", round]]

    def get_match_data(self, tour_rounds_results, mode):
        """Returns list of player_pairs or list of player_scores"""
        player_scores = {}
        player_pairs = []

        for round_result in tour_rounds_results:
            round_name, matches = round_result

            for match in matches:
                match_dates, players, scores = match
                player1 = players[0]
                player2 = players[1]
                player1_id, player1_first_name, player1_last_name, _ = player1
                player2_id, player2_first_name, player2_last_name, _ = player2
                score_j1, score_j2 = scores

                if player1_id not in player_scores:
                    player_scores[player1_id] = {
                        'id': player1_id,
                        'first_name': player1_first_name,
                        'last_name': player1_last_name,
                        'score': 0
                    }

                if player2_id not in player_scores:
                    player_scores[player2_id] = {
                        'id': player2_id,
                        'first_name': player2_first_name,
                        'last_name': player2_last_name,
                        'score': 0
                    }

                player_pair = [player1_id, player2_id]
                player_pairs.append(player_pair)
                player_scores[player1_id]['score'] += score_j1
                player_scores[player2_id]['score'] += score_j2

        if mode == "rank":
            return player_scores

        elif mode == "pairs":
            return player_pairs

    def players_ranks(self, tour_rounds_results):
        """Returns a list of players by score"""
        player_scores = self.get_match_data(tour_rounds_results, "rank")
        results = []

        for player_id, player_data in player_scores.items():
            player_info = [
                player_data['id'], player_data['first_name'],
                player_data['last_name'], player_data['score']
            ]
            results.append(player_info)

        results.sort(key=lambda x: x[3], reverse=True)

        return results

    def prepare_next_round(self, tournament):
        """Prepare le prochain round"""
        self.view.new_header(8)
        tour_rounds_results = tournament.rounds_results
        players_ranks = self.players_ranks(tour_rounds_results)
        tour_round = len(tour_rounds_results) + 1
        round_content = []
        previous_pairs = self.get_match_data(tour_rounds_results, "pairs")
        available_players = players_ranks.copy()

        while available_players:
            # trouver un adversaire qui n'a pas déjà joué contre player1
            player1 = available_players.pop(0)

            for idx, potential_opponent in enumerate(available_players):
                if (
                    [player1, potential_opponent] not in previous_pairs and
                    [potential_opponent, player1] not in previous_pairs
                ):
                    player2 = available_players.pop(idx)
                    break

                else:
                    # si tous les joueurs restants ont déjà joué contre player1, choisir un adversaire aléatoire
                    player2 = available_players.pop(0)

            round_content.append([
                ["", ""],
                [
                    [player1[0], player1[1], player1[2], player1[3]],
                    [player2[0], player2[1], player2[2], player2[3]]
                ],
                [-1, -1]
            ])

            previous_pairs.append([player1[0], player2[0]])

        tour_rounds_results.append([f"Round {tour_round}", round_content])
        tournament.round = tour_round
        tournament.rounds_results = tour_rounds_results
        TournamentDataManager().update_tournament(tournament)
        self.resume_tournament(tournament)

    def tournament_results(self, tournament):
        """Prepare l'affichage des scores finaux"""
        tour_name = tournament.tournament_name
        tour_city = tournament.city
        tour_beg = tournament.beg_date
        tour_end = datetime.now().strftime('%Y-%m-%d_%H:%M')
        players_ranks = self.players_ranks(tournament.rounds_results)
        tournament.final_results = players_ranks
        tournament.end_date = tour_end
        TournamentDataManager().update_tournament(tournament)
        self.view.new_header(8)
        self.view.display_table(
            "tournament_final_rank", players_ranks,
            additional_info=(tour_name, tour_city, tour_beg, tour_end)
        )
        self.view.user_prompts(19, ["", ""])

    def tournament_display(self, tour_title, tour_city, tour_round, tour_rounds, current_round):
        """Affichage des matchs"""
        self.view.new_header(8)
        self.view.notify_alert(17, [tour_title, tour_city])
        self.view.notify_alert(18, [tour_round, tour_rounds])
        self.view.display_table("round_matches", current_round)

    def auto_score(self, tournament, current_round, current_round_index):
        """Demande si on veut des scores aleatoires (debug func)"""
        while True:
            auto_prompt = self.user_confirm(22)
            if auto_prompt:
                # remplissage automatique des scores
                current_date = datetime.now().strftime("%Y-%m-%d_%H:%M")

                for match in current_round[1]:
                    if match[0][1] == "":
                        score_1 = random.choice([0.0, 0.5, 1.0])
                        score_2 = 0.0 if score_1 == 1.0 else 1.0 if score_1 == 0.0 else 0.5
                        match[0][1] = current_date
                        random_minutes = random.randint(5, 50)
                        time_difference = timedelta(minutes=random_minutes)
                        match_start = datetime.strptime(current_date, '%Y-%m-%d_%H:%M') - time_difference
                        match[0][0] = match_start.strftime('%Y-%m-%d_%H:%M')
                        match[2][0] = score_1
                        match[2][1] = score_2

                tournament.rounds_results[current_round_index] = current_round
                TournamentDataManager().update_tournament(tournament)
                break

            else:
                break

    def resume_tournament(self, tournament):
        """Reprends le tournoi en cours"""
        tour_title = tournament.tournament_name
        tour_city = tournament.city
        tour_rounds = tournament.rounds
        tour_round = tournament.round
        tour_rounds_results = tournament.rounds_results
        current_round_index = tour_round - 1
        current_round = tour_rounds_results[current_round_index]
        self.tournament_display(tour_title, tour_city, tour_round, tour_rounds, current_round[1])

        if AUTOMATIC_FILL:
            if all(match[2][0] == -1 for match in current_round[1]):
                self.auto_score(tournament, current_round, current_round_index)

        while any(match[0][1] == "" for match in current_round[1]):
            # remplissage manuel des scores de chaque match d'un round
            self.tournament_display(tour_title, tour_city, tour_round, tour_rounds, current_round[1])

            while True:
                max_index = len(current_round[1]) - 1
                match_index = self.view.user_prompts(24, ["", ""])
                if match_index.isdigit():
                    match_index = int(match_index) - 1
                    if 0 <= match_index <= max_index:
                        selected_match = current_round[1][match_index]
                        if selected_match[0][1] != "":
                            self.view.notify_alert(33, ["", ""])
                            choice = self.user_confirm(5)

                            if choice:
                                break

                        else:
                            break

                    else:
                        self.view.invalid_input(14, ["", ""])

                else:
                    if match_index == "q":
                        return
                    else:
                        self.view.invalid_input(14, ["", ""])

            if selected_match[0][0] == "":  # start the match
                selected_match[0][0] = datetime.now().strftime('%Y-%m-%d_%H:%M')

            else:  # enter score of match
                while True:
                    try:
                        match_p1 = f"{selected_match[1][0][1]} {selected_match[1][0][2]}"
                        match_p2 = f"{selected_match[1][1][1]} {selected_match[1][1][2]}"
                        score = int(self.view.user_prompts(25, [f"{match_p1}", f"{match_p2}"]))
                        if 0 <= score <= 2:
                            break

                        else:
                            self.view.invalid_input(15, ["", ""])

                    except ValueError:
                        self.view.invalid_input(15, ["", ""])

                # Mettre à jour les scores et la date de fin de match
                selected_match[2][0] = 0.5 if score == 0 else 1.0 if score == 1 else 0.0
                selected_match[2][1] = 0.5 if score == 0 else 1.0 if score == 2 else 0.0
                selected_match[0][1] = datetime.now().strftime('%Y-%m-%d_%H:%M')

            tournament.rounds_results[current_round_index] = current_round
            TournamentDataManager().update_tournament(tournament)

        self.tournament_display(tour_title, tour_city, tour_round, tour_rounds, current_round[1])

        if tour_round < tour_rounds:
            self.view.user_prompts(17, ["", ""])
            self.prepare_next_round(tournament)

        else:
            self.view.user_prompts(18, ["", ""])
            self.tournament_results(tournament)
