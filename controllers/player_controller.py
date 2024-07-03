from views.views import MainView
#from controllers.main_controller import MainController
from models.players_models import PlayerModel
from controllers.report_controller import ReportController
from datetime import datetime, timedelta
import random
import string
import json
import os
import re

class PlayerController:
    '''Contrôleur de gestion des joueurs'''

    def __init__(self):
        pass

    def player_menu(self):
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView.clear_screen()
                MainView().player_menu()
            
            choice = MainView().pick_option()
            
            if choice in ["1", "2", "3", "4"]:
                invalid_input = 0
                if choice == "1":  # self.create_player()
                    self.create_player()
                elif choice == "2":  # self.edit_player()
                    self.edit_player()
                elif choice == "3":  # ReportController.list_players()
                    ReportController.list_all_players()
                elif choice == "4":  # main menu
                    break
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0, ["", ""])
    
    def player_data(self):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
    
    def create_player(self):
        MainView.clear_screen()
        MainView().menu_header(5)
        player_id, first_name, last_name, birth_date = PlayerController.get_player_details("create")
        player = PlayerModel(player_id, first_name, last_name, birth_date)
        PlayerModel.save_new_player(player)
        MainView().notify_alert(2, ["", ""])
        MainView().user_prompts(4, ["", ""])
    
    def edit_player(self):
        MainView.clear_screen()
        MainView().menu_header(6)
        player_id, first_name, last_name, birth_date = PlayerController.get_player_details("edit")
        player = PlayerModel(player_id, first_name, last_name, birth_date)
        PlayerModel.update_player(player)
        MainView().notify_alert(4, ["", ""])
        MainView().user_prompts(0, ["", ""])
        
    
    @staticmethod
    def vali_date(date_input):
        ''' returns date input normalisée, is_valid bool, notify_index int '''
        formats = [
            r"(\d{4})(\d{2})(\d{2})",
            r"(\d{4}) (\d{2}) (\d{2})",
            r"(\d{4})-(\d{2})-(\d{2})",
            r"(\d{4})\.(\d{2})\.(\d{2})",
            r"(\d{4}),(\d{2}),(\d{2})",
            r"(\d{4})/(\d{2})/(\d{2})"
        ]
        for fmt in formats:
            match = re.match(fmt, date_input)
            if match:
                year, month, day = map(int, match.groups())
                try:
                    birth_date = datetime(year, month, day)
                    today = datetime.now()
                    if birth_date > today:
                        return date_input, False, 3
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    if age > 150:
                        return date_input, False, 4
                    elif age < 4:
                        return date_input, False, 5
                    return birth_date.strftime('%Y-%m-%d'), True, 0
                except ValueError:
                    return date_input, False, 3
        return date_input, False, 3

    def get_player_details(mode):
        while True:
            player_id = MainView().user_prompts(1, ["", ""])
            if re.match(r"[A-Z]{2}\d{5}", player_id) and len(player_id) == 7:
                if mode == "create":
                    if not PlayerModel.id_exists(player_id):
                        break
                    else:
                        MainView().notify_alert(0, ["", ""])
                elif mode == "edit":
                    if PlayerModel.id_exists(player_id):
                        break
                    else:
                        MainView().notify_alert(3, ["", ""])
                elif mode == "tournament":
                    break
                
            else:
                MainView().invalid_input(6, ["", ""])
            
        while True:
            first_name = MainView().user_prompts(2, ["", ""])
            if first_name and first_name.replace("-", "").isalpha():
                break
            MainView().invalid_input(1, ["", ""])
        
        while True:
            last_name = MainView().user_prompts(3, ["", ""])
            if last_name and last_name.replace("-", "").isalpha():
                break
            MainView().invalid_input(2, ["", ""])

        while True:
            birth_date = MainView().user_prompts(4, ["", ""])
            valid_date = PlayerController.vali_date(birth_date)
            if valid_date[1]:
                birth_date = valid_date[0]
                break
            MainView().invalid_input(valid_date[2], ["", ""])
    
        return player_id, first_name, last_name, birth_date
    
    def generate_random_id():
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=2))
            digits = ''.join(random.choices(string.digits, k=5))
            player_id = letters + digits
            if not PlayerModel.id_exists(player_id):
                return player_id
    
    def generate_random_date():
        ''' génère une date aléatoire entre -8 et -120 ans '''
        current_year = datetime.now().year
        start_year = current_year - 120
        end_year = current_year - 8
        start_date = datetime(year=start_year, month=1, day=1)
        end_date = datetime(year=end_year, month=12, day=31)
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")
    
    def generate_random_players(number_of_players):
        tournament_players = []
        file_path = 'data/randomizer.json'
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                random_data = json.load(file)
                fr_names = random_data.get('noms_fr', None)
                en_names = random_data.get('noms_en', None)
            
            for n in range(number_of_players):
                player_id = PlayerController.generate_random_id()
                a = random.choice(["fr","en"])
                if a == "fr":
                    prenom = random.choice(fr_names[0])
                    nom = random.choice(fr_names[1])
                else:
                    prenom = random.choice(en_names[0])
                    nom = random.choice(en_names[1])
                first_name = prenom
                last_name = nom
                birth_date = PlayerController.generate_random_date()
                new_player = [player_id, first_name, last_name, birth_date]
                tournament_players.append(new_player)
            
            return tournament_players
            
        else:
            MainView().notify_alert(8, [file_path,""])
            MainView().user_prompts(0, ["", ""])
            return []