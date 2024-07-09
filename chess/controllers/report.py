from views.main import MainView
from controllers import main
from models.player import PlayerModel
from models.player import PlayerDataManager
from prettytable import PrettyTable
from datetime import datetime
from tinydb import TinyDB, Query
import os

class ReportController:
    '''Contrôleur de gestion des rapports'''

    def __init__(self):
        pass

    def report_menu(self):
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView.clear_screen()
                MainView().report_menu()
            
            choice = MainView().pick_option()
            
            if choice in ["1", "2", "3" ,"4" ,"5" ,"6"]:
                invalid_input = 0
                if choice == "1":  # self.list_players()
                    self.list_all_players()
                elif choice == "2":  # self.list_tournaments()
                    self.list_tournaments()
                elif choice == "3":  # self.get_tournament_info()
                    pass
                elif choice == "4":  # self.get_tournament_players()
                    pass
                elif choice == "5":  # self.get_tournament_matches()
                    pass
                elif choice == "6":  # main menu
                    break
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0)
    
    def list_all_players(self):
        MainView.clear_screen()
        MainView().menu_header(9)
        players_list = PlayerDataManager().list_players("last_name")  # option to sort by "last_name", "player_id", "birth_date"...
        self.report_player_list_to_drive(players_list)
        total_players = len(players_list)
        if total_players > 20:
            self.report_player_pages(players_list)
        else:
            MainView().report_player_list(players_list)
        
        MainView().notify_alert(15, ["", ""])
        MainView().notify_alert(16, ["", ""])
        MainView().user_prompts(0, ["", ""])
    
    def report_player_list_to_drive(self, file_data):
        if os.path.exists("data"):
            report_path = 'data/reports/full_chess_club_players_list.txt'
        else:
            report_path = 'chess/data/reports/full_chess_club_players_list.txt'
            
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        myTable = PrettyTable(["ID", "Prénom", "Nom", "Ddn"])
        with open(report_path, 'w') as report_file:
            for data in file_data:
                player_id = data.get("player_id", "N/A")
                first_name = data.get("first_name", "N/A")
                last_name = data.get("last_name", "N/A")
                birth_date = data.get("birth_date", "N/A")
                myTable.add_row([player_id, first_name, last_name, birth_date])
        
            report_file.write(myTable.get_string())
    
    def report_player_pages(self, players_list):
        page_size = 20
        total_players = len(players_list)
        total_pages = (total_players // page_size) + (1 if total_players % page_size != 0 else 0)
        
        for page in range(total_pages):
            MainView.clear_screen()
            MainView().menu_header(9)
            
            start_index = page * page_size
            end_index = start_index + page_size
            page_data = players_list[start_index:end_index]
            MainView().report_player_list(page_data)
            
            if page < total_pages - 1:
                MainView().user_prompts(14, [page + 1, total_pages])
    
    def list_tournaments(self):
        if os.path.exists("data"):
            relative_path = 'data/'
        else:
            relative_path = 'chess/data/'
        
        pending_tournament_path = (f"{relative_path}pending_tournament.json")
        old_tournaments_path =(f"{relative_path}tournaments/")
        
        tournaments = []

        # Vérifier le fichier pending_tournament.json
        if os.path.exists(pending_tournament_path):
            with open(pending_tournament_path, 'r', encoding='utf-8') as f:
                db = TinyDB(pending_tournament_path)
                tournament_table = db.table('tournament')
                tournament = tournament_table.all()
                if tournament:
                    tournament = tournament[0]
                    tournament_info = {
                        "name": tournament.get("tournament_name", "Unknown"),
                        "start_date": tournament.get("beg_date", "Unknown"),
                        "end_date": tournament.get("end_date", "Unknown"),
                        "city": tournament.get("city", "Unknown")
                    }
                    tournaments.append(tournament_info)
                db.close()

        # Parcourir tous les fichiers dans le dossier tournaments
        if os.path.exists(old_tournaments_path):
            for filename in os.listdir(old_tournaments_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(old_tournaments_path, filename)
                    db = TinyDB(file_path)
                    tournament_table = db.table('tournament')
                    tournament = tournament_table.all()
                    if tournament:
                        tournament = tournament[0]
                        tournament_info = {
                            "name": tournament.get("tournament_name", "Unknown"),
                            "start_date": tournament.get("beg_date", "Unknown"),
                            "end_date": tournament.get("end_date", "Unknown"),
                            "city": tournament.get("city", "Unknown")
                        }
                        tournaments.append(tournament_info)
                    db.close()

        # Afficher les informations des tournois
        MainView().report_tournament_list(tournaments)
        MainView().user_prompts(0, ["", ""])