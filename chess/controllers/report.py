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
        self.view = MainView()

    def report_menu(self):
        """ menu des rapports """
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
                self.view.invalid_input(0)
    
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
        self.view.clear_screen()
        self.view.menu_header(9)
        if self.data_file_exists("players"):
            # option pour ranger par "last_name", "player_id", "birth_date"...
            players_list = PlayerDataManager().list_players("last_name")
            self.report_player_list_to_drive(players_list)
            total_players = len(players_list)
            
            if total_players > 20:
                self.report_player_pages(players_list)
            else:
                self.view.display_table("player_list", players_list)
            
            self.view.notify_alert(15, ["", ""])
            self.view.notify_alert(16, ["", ""])
            self.view.user_prompts(0, ["", ""])
        else:
            self.view.clear_screen()
            self.view.menu_header(9)
            self.view.notify_alert(11, ['data/players.json', ""])
            self.view.user_prompts(0, ["", ""])
    
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
            self.view.clear_screen()
            self.view.menu_header(9)
            start_index = page * page_size
            end_index = start_index + page_size
            page_data = players_list[start_index:end_index]
            self.view.display_table("player_list", page_data)
            
            if page < total_pages - 1:
                self.view.user_prompts(14, [page + 1, total_pages])
    
    def report_rounds_pages(self, round_results, tour_info):
        """ créé des pages pour l'affichage des tableaux de rounds """
        total_pages = len(round_results)
        for page in range(total_pages):
            self.view.clear_screen()
            self.view.menu_header(13)
            self.view.notify_alert(22, [tour_info[0], tour_info[1]])
            self.view.notify_alert(23, [page + 1, ""])
            self.view.display_table("match_list", round_results[page][1])
            
            if page < total_pages - 1:
                self.view.user_prompts(14, [page + 1, total_pages])
    
    def get_tournament_data(self, path):
        """ returns tournament_data dictionnary """
        db = TinyDB(path)
        tournaments_table = db.table('tournaments')
        tournaments = tournaments_table.all()
        db.close()
        return tournaments
    
    def list_tournaments(self):
        """ returns list of tournaments """
        if os.path.exists("data"):
            relative_path = 'data/'
        else:
            relative_path = 'chess/data/'
        
        tournaments_path = f"{relative_path}tournaments.json"
        tournaments = []
        
        # vérifier tournaments.json
        if os.path.exists(tournaments_path):
            with open(tournaments_path, 'r', encoding='utf-8') as f:
                tournaments = self.get_tournament_data(tournaments_path)
        
        return tournaments
    
    def list_all_tournaments(self):
        """ lister les tournois """
        tournaments = self.list_tournaments()
        self.view.clear_screen()
        self.view.menu_header(10)
        n_tour = len(tournaments)
        if n_tour > 0:
            self.view.display_table("tournament_list", tournaments)
        else:
            self.view.notify_alert(21, ["", ""])
        
        self.view.user_prompts(0, ["", ""])
    
    def get_tournament_info(self, mode):
        """ extraire les data d'un tournoi """
        tournaments = self.list_tournaments()
        self.view.clear_screen()
        self.view.menu_header(10)
        n_tour = len(tournaments)
        if n_tour > 0:
            self.view.display_table("pick_tournament", tournaments)
            while True:
                try:
                    choice = int(self.view.user_prompts(20, ["", ""]))
                    if 1 <= choice <= n_tour:
                        choice = choice - 1
                        self.view.clear_screen()
                        tournament_data = [tournaments[choice]]
                        if mode == "tour":
                            self.view.menu_header(11)
                            self.view.display_table("tournament_list", tournament_data)
                        elif mode == "players":
                            self.view.menu_header(12)
                            for data in tournament_data:
                                players_list = data['players']
                            
                            players_list = self.transform_player_list(players_list)  # list to dict
                            total_players = len(players_list)
                            
                            if total_players > 20:
                                self.report_player_pages(players_list)
                            else:
                                self.view.display_table("player_list", players_list)

                        elif mode == "matches":
                            self.view.menu_header(13)
                            for data in tournament_data:
                                round_results = data['rounds_results']
                            
                            tour_info = [tournament_data[0].get('tournament_name'), tournament_data[0].get('city')]
                            self.report_rounds_pages(round_results, tour_info)
                            final_results = tournament_data[0].get('final_results')
                            if len(final_results) > 0:
                                self.view.user_prompts(18, ["", ""])
                                self.view.clear_screen()
                                self.view.menu_header(13)
                                tour_beg = tournament_data[0].get('beg_date')
                                tour_end = tournament_data[0].get('end_date')
                                self.view.display_table("tournament_final_rank", final_results, 
                                                    additional_info=(tour_info[0], tour_info[1], tour_beg, tour_end))
                        
                        break
                    
                    else:
                        self.view.invalid_input(13, ["", ""])
                    
                except ValueError:
                    self.view.invalid_input(13, ["", ""])
                
        else:
            self.view.notify_alert(21, ["", ""])
        
        self.view.user_prompts(0, ["", ""])
    