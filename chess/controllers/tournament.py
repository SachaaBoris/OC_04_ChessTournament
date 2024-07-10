from views.main import MainView
from controllers.player import PlayerController
from controllers.report import ReportController
from models.player import PlayerModel
from models.player import PlayerDataManager
from models.tournament import Tournament
from models.tournament import TournamentDataManager
from itertools import combinations
from datetime import datetime
import random
import json
import os
import re


class TournamentController:
    """Contrôleur de gestion des tournois"""

    def __init__(self):
        pass
        
    def tournament_menu(self):
        """ menu de gestion des tournois """
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView().clear_screen()
                MainView().tournament_menu()
            
            choice = MainView().user_prompts(21, ["", ""])

            if choice in ["1", "2", "3", "4"]:
                invalid_input = 0
                if choice == "1":
                    self.create_tournament()  # self.create_tournament()
                elif choice == "2":
                    self.can_resume_tournament()  # self.launch_tournament()
                elif choice == "3":
                    ReportController().list_tournaments()  # ReportController().list_tournaments()
                elif choice == "4":
                    break  # main menu
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0, ["", ""])
    
    def data_file_exists(self, file_name):
        """ returns bool """
        if os.path.exists("data"):
            file_path = f'data/{file_name}.json'
        else:
            file_path = f'chess/data/{file_name}.json'
        if os.path.isfile(file_path):
            return True
        else:
            return False
        
    def generate_random_tour_title_city(self):
        """ returns [str(tour_name), str(tour_city)] """
        if self.data_file_exists("randomizer"):
            if os.path.exists("data"):
                file_path = 'data/randomizer.json'
            else:
                file_path = 'chess/data/randomizer.json'
            with open(file_path, 'r', encoding='utf-8') as file:
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
        """ menu de creation de tournoi """
        MainView().clear_screen()
        MainView().menu_header(7)
        save = True
        if self.data_file_exists("pending_tournament"):
            save = False
            MainView().notify_alert(5, ["", ""])
            sure = MainView().user_prompts(5, ["", ""])
            if sure in ["y", "yes", "o", "oui"]:
                save = True
        
        if save:
            tournament_details = self.get_tournament_details()
            print("Titre: ", tournament_details[0])
            print("Ville: ", tournament_details[1])
            TournamentDataManager().save_new_tournament(tournament_details)          
            MainView().notify_alert(9, ["", ""])
            MainView().user_prompts(0, ["", ""])
    
    def get_tournament_details(self):
        """ returns [tournament_details_list] """
        number_of_players = self.get_tournement_how_many_players()
        tour_players = self.get_tournament_automatic(number_of_players)
        
        if len(tour_players) == 0:
            for n in range(number_of_players):
                MainView().notify_alert(7, [n + 1, number_of_players])
                new_player = [PlayerController().get_player_details("tournament")]
                tour_players.append(new_player)
        
            tour_rounds = self.get_tournament_rounds()
            tour_desc = MainView().user_prompts(11, ["", ""])
            tour_city = MainView().user_prompts(12, ["", ""])
            tour_title = MainView().user_prompts(13, ["", ""])
        else:
            tour_rounds = self.get_tournament_rounds()
            tour_desc = ""
            title_city = self.generate_random_tour_title_city()
            tour_title = title_city[0]
            tour_city = title_city[1]  
        
        tournament_details = []
        if len(tour_players) > 0:
            PlayerDataManager().save_player_list(tour_players)
        
            # initialisation de valeures vides
            tour_round = 0
            tour_rounds_results = []
            tour_final_results = []
            tour_beg_date = ""
            tour_end_date = ""
            
            tournament_details = [
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
            
        return tournament_details
    
    def get_tournement_how_many_players(self):
        """ returns int number_of_players """
        while True:   
            try:
                number_of_players = int(MainView().user_prompts(6, ["", ""]))
                if 8 <= number_of_players <= 98:
                    break
                else:
                    MainView().invalid_input(7, ["", ""])
            except ValueError:
                MainView().invalid_input(7, ["", ""])
        
        return number_of_players
    
    def get_tournament_automatic(self, number_of_players):
        """ returns list of tournament players """
        tour_players = []
        while True:
            automatic = MainView().user_prompts(7, ["", ""])
            if automatic in ["y", "yes", "o", "oui"]:
                MainView().notify_alert(6, ["", ""])
                sure = MainView().user_prompts(5, ["", ""])
                if sure in ["y", "yes", "o", "oui"]:
                    tour_players = PlayerController().generate_random_players(number_of_players)
                    break
                else:
                    break
            else:
                break
        
        return tour_players
    
    def get_tournament_rounds(self):
        """ returns int(tour_rounds) """
        while True:
            tour_rounds = MainView().user_prompts(10, ["", ""])
            if tour_rounds in ["0", ""]:
                tour_rounds = "4"
            try:
                tour_rounds = int(tour_rounds)
                if 1 <= tour_rounds <= 99:
                    break
                else:
                    MainView().invalid_input(11, ["", ""])
            except ValueError:
                MainView().invalid_input(11, ["", ""])
        
        return tour_rounds
    
    def can_resume_tournament(self):
        """ verifie le statue de pending_tournament """
        MainView().clear_screen()
        MainView().menu_header(8)
        if self.data_file_exists("pending_tournament"):
            self.tournament_status()
        else:
            MainView().notify_alert(10, ["", ""])
            MainView().user_prompts(0, ["", ""])
    
    def tournament_status(self):
        """ détermine quel methode appliquer pour reprendre le tournoi """
        if TournamentDataManager().has_tournament_started():
            self.resume_tournament([])
        else:
            self.start_tournament()
    
    def db_get_tournament_data(self):
        """ returns list of tournament_details """
        tournament_data = TournamentDataManager().get_tournament_data()
        tour_title = tournament_data[0].get('tournament_name')
        tour_city = tournament_data[0].get('city')
        tour_desc = tournament_data[0].get('description')
        tour_players = tournament_data[0].get('players')
        tour_rounds = tournament_data[0].get('rounds')
        tour_round = tournament_data[0].get('round')
        tour_rounds_results = tournament_data[0].get('rounds_results')
        tour_final_results = tournament_data[0].get('final_results')
        tour_beg_date = tournament_data[0].get('beg_date')
        tour_end_date = tournament_data[0].get('end_date')
        tournament_details = [
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
        return tournament_details
    
    def start_tournament(self):
        """ démarre le tournoi """
        tournament_data = self.db_get_tournament_data()
        tour_round = 1
        tour_rounds_results = self.prepare_first_round(tournament_data[3])
        tour_beg_date = datetime.now().strftime('%Y-%m-%d_%H:%M')
        
        tournament_details = [
            tournament_data[0], 
            tournament_data[1], 
            tournament_data[2], 
            tournament_data[3], 
            tournament_data[4], 
            tour_round, 
            tour_rounds_results, 
            tournament_data[7], 
            tour_beg_date, 
            tournament_data[9]
        ]
        TournamentDataManager().update_tournament(tournament_details)
        self.resume_tournament(tournament_details)
    
    def prepare_first_round(self, players):
        """ returns list [first_round] """
        randomised_players = random.shuffle(players)
        round = []
        for i in range(0, len(players), 2):
            round.append([["", ""], [players[i], players[i+1]], [-1, -1]])

        return [["Round 1", round]]
    
    def get_match_data(self, tour_rounds_results, mode):
        """ returns list of player_pairs or list of player_scores """
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
        """ returns a list of players by score """
        player_scores = self.get_match_data(tour_rounds_results, "rank")

        results = []
        for player_id, player_data in player_scores.items():
            player_info = [player_data['id'], player_data['first_name'], player_data['last_name'], player_data['score']]
            results.append(player_info)

        results.sort(key=lambda x: x[3], reverse=True)
        
        return results
    
    def prepare_next_round(self, tournament_data):
        """ prepares next round """
        MainView().clear_screen()
        MainView().menu_header(8)
        players = tournament_data[3]
        players_ranks = self.players_ranks(tournament_data[6])
        tour_rounds_results = tournament_data[6]
        tour_pairs = self.get_match_data(tour_rounds_results, "pairs")
        tour_round = len(tournament_data[6])+1
        round_content = []

        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i+1]
            
            # Vérification si les joueurs ont déjà joué ensemble
            while [player1, player2] in tour_pairs or [player2, player1] in tour_pairs:
                player1, player2 = random.sample(players, 2)  # Sélection aléatoire de deux joueurs
            
            # Ajout des paires avec scores initiaux
            round_content.append([["", ""], [[player1[0], player1[1], player1[2], player1[3]],
                                [player2[0], player2[1], player2[2], player2[3]]], [-1, -1]])

            # Ajout des paires à la liste des paires de tournois pour empêcher la répétition des matchs
            tour_pairs.append([player1, player2])

        tour_rounds_results.append([f"Round {tour_round}", round_content])
        
        tournament_details = [
            tournament_data[0], 
            tournament_data[1], 
            tournament_data[2], 
            tournament_data[3], 
            tournament_data[4], 
            tour_round, 
            tour_rounds_results, 
            tournament_data[7], 
            tournament_data[8],
            tournament_data[9]
        ]
        
        TournamentDataManager().update_tournament(tournament_details)
        self.resume_tournament(tournament_details)
    
    def tournament_results(self, tournament_data):
        """ prepare l'affichage des scores finaux """
        players_ranks = self.players_ranks(tournament_data[6])
        tour_end_date = datetime.now().strftime('%Y-%m-%d_%H:%M')
        tournament_details = [
            tournament_data[0], 
            tournament_data[1], 
            tournament_data[2], 
            tournament_data[3], 
            tournament_data[4], 
            tournament_data[5], 
            tournament_data[6], 
            players_ranks, 
            tournament_data[8],
            tour_end_date
        ]
        TournamentDataManager().update_tournament(tournament_details)
        TournamentDataManager().close_tournament(tournament_data[1], tournament_data[8])
        MainView().clear_screen()
        MainView().menu_header(8)
        MainView().tournament_final_rank(tournament_data[0], tournament_data[1],
                                         tournament_data[8], tour_end_date, players_ranks)
        MainView().user_prompts(19, ["", ""])
    
    def resume_tournament(self, tournament_details):
        """ reprends le tournoi en cours """
        if len(tournament_details) == 0:
            tournament_details = self.db_get_tournament_data()
        
        tour_title = tournament_details[0]
        tour_city = tournament_details[1]
        tour_desc = tournament_details[2]
        tour_players = tournament_details[3]
        tour_rounds = tournament_details[4]
        tour_round = tournament_details[5]
        tour_rounds_results = tournament_details[6]
        tour_final_results = tournament_details[7]
        tour_beg_date = tournament_details[8]
        tour_end_date = tournament_details[9]
        
        number_of_matches = int(len(tour_players)/2)
        updated_rounds_results = tour_rounds_results
        
        for i, tour_round_result in enumerate(tour_rounds_results):
            round_name, matches = tour_round_result
            tour_round = i + 1
            for j, match in enumerate(matches):
                match_dates, players, scores = match
                round_match = j + 1
                if match_dates[0] == "" or match_dates[1] == "":
                    player1 = players[0]
                    player2 = players[1]
                    p1name = f"{player1[1]} {player1[2]}"
                    p2name = f"{player2[1]} {player2[2]}"
                    
                    MainView().notify_alert(17, [tour_title, tour_city])
                    MainView().notify_alert(18, [tour_round, tour_rounds])
                    MainView().notify_alert(19, [round_match, number_of_matches])
                    MainView().user_prompts(15, [p1name, p2name])
                    start_time = datetime.now().strftime("%Y-%m-%d_%H:%M")
                    MainView().clear_screen()
                    MainView().menu_header(8)
                    MainView().notify_alert(17, [tour_title, tour_city])
                    MainView().notify_alert(18, [tour_round, tour_rounds])
                    MainView().notify_alert(19, [round_match, number_of_matches])
                    MainView().notify_alert(20, [p1name, p2name])
                    score_j1 = MainView().user_prompts(16, [p1name, ""])

                    while not re.match(r'^(0|0\.5|1)$', score_j1):
                        MainView().invalid_input(12, ["", ""])
                        score_j1 = MainView().user_prompts(16, [p1name, ""])

                    score_j1 = float(score_j1)
                    score_j2 = 1.0 - score_j1 if score_j1 in [0, 1] else 0.5
                    scores = [score_j1, score_j2]

                    end_time = datetime.now().strftime("%Y-%m-%d_%H:%M")
                    matches[j][0] = [start_time, end_time]

                    updated_rounds_results[i][1][j] = [[start_time, end_time], players, scores]
                    tournament_details = [
                        tour_title,
                        tour_city,
                        tour_desc,
                        tour_players,
                        tour_rounds,
                        tour_round,
                        updated_rounds_results,
                        tour_final_results,
                        tour_beg_date,
                        tour_end_date,
                    ]
                    TournamentDataManager().update_tournament(tournament_details)
                    MainView().clear_screen()
                    MainView().menu_header(8)
        
        if tour_round < tour_rounds:
            MainView().clear_screen()
            MainView().menu_header(8)
            MainView().user_prompts(17, ["", ""])
            self.prepare_next_round(tournament_details)
        else:
            MainView().clear_screen()
            MainView().menu_header(8)
            MainView().user_prompts(18, ["", ""])
            self.tournament_results(tournament_details)
    