from views.main import MainView
from controllers import main
from models.player import PlayerModel
from models.player import PlayerDataManager
from prettytable import PrettyTable
from datetime import datetime
from tinydb import TinyDB, Query
import os


class ReportController:
    """Contrôleur de gestion des rapports"""

    def __init__(self):
        pass

    def report_menu(self):
        """ menu des rapports """
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView().clear_screen()
                MainView().report_menu()
            
            choice = MainView().user_prompts(21, ["", ""])
            
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
                MainView().invalid_input(0)
    
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
    
    def transform_player_list(self, player_list):
        """ returns sorted dictionary """
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
        """ lister tous les joueurs """
        MainView().clear_screen()
        MainView().menu_header(9)
        if self.data_file_exists("players"):
            # option to sort by "last_name", "player_id", "birth_date"...
            players_list = PlayerDataManager().list_players("last_name")
            self.report_player_list_to_drive(players_list)
            total_players = len(players_list)
            
            if total_players > 20:
                self.report_player_pages(players_list)
            else:
                MainView().report_player_list(players_list)
            
            MainView().notify_alert(15, ["", ""])
            MainView().notify_alert(16, ["", ""])
            MainView().user_prompts(0, ["", ""])
        else:
            MainView().clear_screen()
            MainView().menu_header(9)
            MainView().notify_alert(11, ['data/players.json', ""])
            MainView().user_prompts(0, ["", ""])
    
    def report_player_list_to_drive(self, file_data):
        """ enregistre le rapport """
        if os.path.exists("data"):
            report_path = 'data/reports/full_chess_club_players_list.txt'
        else:
            report_path = 'chess/data/reports/full_chess_club_players_list.txt'

        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        my_table = PrettyTable(["ID", "Prénom", "Nom", "Ddn"])
        with open(report_path, 'w') as report_file:
            for data in file_data:
                player_id = data.get("player_id", "N/A")
                first_name = data.get("first_name", "N/A")
                last_name = data.get("last_name", "N/A")
                birth_date = data.get("birth_date", "N/A")
                my_table.add_row([player_id, first_name, last_name, birth_date])
        
            report_file.write(my_table.get_string())
    
    def report_player_pages(self, players_list):
        """ créé des pages pour l'affichage des tableaux de joueurs """
        page_size = 20
        total_players = len(players_list)
        total_pages = (total_players // page_size) + (1 if total_players % page_size != 0 else 0)
        
        for page in range(total_pages):
            MainView().clear_screen()
            MainView().menu_header(9)
            start_index = page * page_size
            end_index = start_index + page_size
            page_data = players_list[start_index:end_index]
            MainView().report_player_list(page_data)
            
            if page < total_pages - 1:
                MainView().user_prompts(14, [page + 1, total_pages])
    
    def report_rounds_pages(self, round_results, tour_info):
        """ créé des pages pour l'affichage des tableaux de rounds """
        total_pages = len(round_results)
        for page in range(total_pages):
            MainView().clear_screen()
            MainView().menu_header(9)
            MainView().notify_alert(22, [tour_info[0], tour_info[1]])
            MainView().notify_alert(23, [page + 1, ""])
            MainView().report_match_list(round_results[page])
            
            if page < total_pages - 1:
                MainView().user_prompts(14, [page + 1, total_pages]) 
    
    def get_tournament_data(self, path):
        """ returns tournament_data dictionnary """
        db = TinyDB(path)
        tournament_table = db.table('tournament')
        tournament = tournament_table.all()
        tournament_data = {}
        if tournament:
            tournament = tournament[0]
            tournament_data = {
                "name": tournament.get("tournament_name", "Unknown"),
                "city": tournament.get("city", "Unknown"),
                "description": tournament.get("description", "Unknown"),
                "players": tournament.get("players", "Unknown"),
                "rounds": tournament.get("rounds", "Unknown"),
                "round": tournament.get("round", "Unknown"),
                "rounds_results": tournament.get("rounds_results", "Unknown"),
                "final_results": tournament.get("final_results", "Unknown"),
                "beg_date": tournament.get("beg_date", "Unknown"),
                "end_date": tournament.get("end_date", "Unknown")
            }
        db.close()
        return tournament_data
    
    def list_tournaments(self):
        """ returns list of tournaments """
        if os.path.exists("data"):
            relative_path = 'data/'
        else:
            relative_path = 'chess/data/'
        
        pending_tournament_path = f"{relative_path}pending_tournament.json"
        old_tournaments_path = f"{relative_path}tournaments/"
        tournaments = []
        
        # vérifier pending_tournament.json
        if os.path.exists(pending_tournament_path):
            with open(pending_tournament_path, 'r', encoding='utf-8') as f:
                tournament_data = self.get_tournament_data(pending_tournament_path)
                tournaments.append(tournament_data)
        
        # parcourir tous les jsons du dossier tournaments
        if os.path.exists(old_tournaments_path):
            for filename in os.listdir(old_tournaments_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(old_tournaments_path, filename)
                    tournament_data = self.get_tournament_data(file_path)
                    tournaments.append(tournament_data)
        
        return tournaments
    
    def list_all_tournaments(self):
        """ lister les tournois """
        tournaments = self.list_tournaments()
        MainView().clear_screen()
        MainView().menu_header(10)
        n_tour = len(tournaments)
        if n_tour > 0:
            MainView().report_tournament_list(tournaments)
        else:
            MainView().notify_alert(21, ["", ""])
        
        MainView().user_prompts(0, ["", ""])
    
    def get_tournament_info(self, mode):
        """ extraire les data d'un tournoi """
        tournaments = self.list_tournaments()
        MainView().clear_screen()
        MainView().menu_header(10)
        n_tour = len(tournaments)
        if n_tour > 0:
            MainView().choose_a_tournament(tournaments)
            while True:
                try:
                    choice = int(MainView().user_prompts(20, ["", ""]))
                    if 1 <= choice <= n_tour:
                        choice = choice - 1
                        MainView().clear_screen()
                        tournament_data = [tournaments[choice]]
                        if mode == "tour":
                            MainView().menu_header(11)
                            MainView().report_tournament_list(tournament_data)
                        elif mode == "players":
                            MainView().menu_header(12)
                            for data in tournament_data:
                                players_list = data['players']
                            
                            players_list = self.transform_player_list(players_list)  # list to dict
                            total_players = len(players_list)
                            
                            if total_players > 20:
                                self.report_player_pages(players_list)
                            else:
                                MainView().report_player_list(players_list)

                        elif mode == "matches":
                            MainView().menu_header(13)
                            for data in tournament_data:
                                round_results = data['rounds_results']
                            
                            tour_info = [tournament_data[0].get('name'), tournament_data[0].get('city')]
                            self.report_rounds_pages(round_results, tour_info)
                        
                        break
                    
                    else:
                        MainView().invalid_input(13, ["", ""])
                    
                except ValueError:
                    MainView().invalid_input(13, ["", ""])
                
        else:
            MainView().notify_alert(21, ["", ""])
        
        MainView().user_prompts(0, ["", ""])
    