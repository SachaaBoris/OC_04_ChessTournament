from views.views import MainView
from controllers import main_controller
from models.players_models import PlayerModel
from datetime import datetime
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
                    # vérifier qu'aucun champ n'est vide et que les champs sont conformes
                    # il faudra aussi vérifier si l'ID entré n'existe pas déjà dans la BDD
                elif choice == "2":  # self.edit_player()
                    pass
                    # vérifier qu'aucun champ n'est vide et que les champs sont conformes
                    # il faudra aussi vérifier que si l'ID entré est différent de l'ID initial
                    # le nouvel ID n'existe pas déjà dans la BDD
                elif choice == "3":  # ReportController.list_players()
                    pass
                elif choice == "4":  # main menu
                    break
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0)
    
    def player_data(self):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
    
    def create_player(self):
        MainView.clear_screen()
        MainView().menu_header(5)
        player_id, first_name, last_name, birth_date = PlayerController.get_player_details()
        player = PlayerModel(player_id, first_name, last_name, birth_date)
        PlayerModel.save_new_player(player)
        MainView().notify_alert(9)
        MainView().user_prompts(4)
    
    @staticmethod
    def vali_date(date_input):
        '''verification et normalisation de l'input de date'''
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

    def get_player_details():
        while True:
            player_id = MainView().user_prompts(0)
            if re.match(r"[A-Z]{2}\d{5}", player_id):
                if not PlayerModel.id_exists(player_id):
                    break
                else:
                    MainView().notify_alert(0)
            else:
                MainView().invalid_input(6)
            
        while True:
            first_name = MainView().user_prompts(1)
            if first_name and first_name.replace("-", "").isalpha():
                break
            MainView().invalid_input(1)
        
        while True:
            last_name = MainView().user_prompts(2)
            if last_name and last_name.replace("-", "").isalpha():
                break
            MainView().invalid_input(2)

        while True:
            birth_date = MainView().user_prompts(3)
            valid_date = PlayerController.vali_date(birth_date)
            if valid_date[1]:
                birth_date = valid_date[0]
                break
            MainView().invalid_input(valid_date[2])
    
        return player_id, first_name, last_name, birth_date
