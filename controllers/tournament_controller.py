from views.views import MainView
#from controllers.main_controller import MainController
from controllers.player_controller import PlayerController
from models.players_models import PlayerModel
from datetime import datetime
import random
import json
import os

class TournamentController:
    '''Contrôleur de gestion des tournois'''

    def __init__(self):
        pass
        
    def tournament_menu(self):
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView.clear_screen()
                MainView().tournament_menu()
            
            choice = MainView().pick_option()

            if choice in ["1", "2", "3", "4"]:
                invalid_input = 0
                if choice == "1":  # self.create_tournament()
                    self.create_tournament()
                elif choice == "2":  # self.launch_tournament()
                    pass
                    # reprendre le pending tournament s'il y en a un
                    # sinon, renvoyer un message demandant de créer un tournoi
                elif choice == "3": # ReportController.list_tournaments()
                    pass
                elif choice == "4":  # main menu
                    break
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0, ["", ""])
    
    def generate_random_tour_title_city():
        file_path = 'data/randomizer.json'
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                random_data = json.load(file)
                tour_titles = random_data.get('tour_titles', None)
                tour_cities = random_data.get('cities', None)
            
            tour_city = random.choice(tour_cities)
            tour_title0 = tour_city.split(",")[0].strip()
            tour_title1 = random.choice(tour_titles[0])
            tour_title2 = random.choice(tour_titles[1])
            yearnow = datetime.today().strftime("%Y")
            a = random.choice([1, 2, 3, 4, 5, 6])
            if a == 1:
                tour_name = f"{tour_title1} Chess {tour_title2}"
            elif a == 2:
                tour_name = f"{tour_title1} Chess {tour_title2} {yearnow[2:]}"
            elif a == 3:
                tour_name = f"{tour_title1} {tour_title2} {yearnow[2:]}"
            elif a == 4:
                tour_name = f"{tour_title0} Chess {tour_title2} {yearnow[2:]}"
            elif a == 5:
                tour_name = f"The {tour_title0} {tour_title1} {tour_title2}"
            else:
                tour_name = f"{tour_title1} {tour_title2}"
            
            return [tour_name, tour_city]
        return ["",""]
    
    def create_tournament(self):
        MainView.clear_screen()
        MainView().menu_header(7)
        file_path = 'data/pending_tournament.json'
        go = True
        if os.path.isfile(file_path):
            go = False
            MainView().notify_alert(5, ["", ""])
            sure = MainView().user_prompts(5, ["", ""])
            if sure in ["y", "yes", "o", "oui"]:
                go = True
        
        if go:
            tournament_details = TournamentController.get_tournement_details()
            print("Titre: ", tournament_details[0])
            print("Ville: ", tournament_details[1])
            print("Description: ", tournament_details[2])
            print("Nombre de rounds: ", tournament_details[4])
            print("Participants: ")
            for participant in tournament_details[3]:
                print("  ID: ", participant[0])
                print("  Nom: ", participant[1])
                print("  Prénom: ", participant[2])
                print("  Date: ", participant[3])
                print("  ----------------------")
            
            MainView().notify_alert(9, ["", ""])
            MainView().user_prompts(9, ["", ""])
    
    def get_tournement_details():
        while True:   
            try:
                number_of_players = int(MainView().user_prompts(6, ["", ""]))
                if 8 <= number_of_players <= 98:
                    break
                else:
                    MainView().invalid_input(7, ["", ""])
            except ValueError:
                MainView().invalid_input(7, ["", ""])
        
        tour_players = []
        while True:
            automatic = MainView().user_prompts(7, ["", ""])  # Random prompt
            if automatic in ["y", "yes", "o", "oui"]:
                MainView().notify_alert(6, ["", ""])
                sure = MainView().user_prompts(5, ["", ""])
                if sure in ["y", "yes", "o", "oui"]:
                    tour_players = PlayerController.generate_random_players(number_of_players)
                    break
                else:
                    break
            else:
                break
        
        if len(tour_players) > 0:
            PlayerModel.save_player_list(tour_players)
            while True:
                try:
                    tour_rounds = int(MainView().user_prompts(10, ["", ""]))
                    if 1 <= tour_rounds <= 20:
                        break
                    else:
                        MainView().invalid_input(11, ["", ""])
                except ValueError:
                    MainView().invalid_input(11, ["", ""])
            
            tour_desc = " "
            title_city = TournamentController.generate_random_tour_title_city()
            tour_title = title_city[0]
            tour_city = title_city[1]
            
        else:
            for n in range(number_of_players):
                MainView().notify_alert(7, [n, number_of_players])
                new_player = [PlayerController().get_player_details("tournament")]
                tour_players.append(new_player)
        
            while True:
                try:
                    tour_rounds = int(MainView().user_prompts(10, ["", ""]))
                    if 1 <= tour_rounds <= 20:
                        break
                    else:
                        MainView().invalid_input(11, ["", ""])
                except ValueError:
                    MainView().invalid_input(11, ["", ""])
            
            tour_desc = MainView().user_prompts(11, ["", ""])
            tour_city = MainView().user_prompts(12, ["", ""])
            tour_title = MainView().user_prompts(13, ["", ""])
        
        return [tour_title, tour_city, tour_desc, tour_players, tour_rounds]
        