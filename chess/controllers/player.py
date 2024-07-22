from views.main import MainView
from models.player import PlayerModel
from models.player import PlayerDataManager
from controllers.report import ReportController
from config_loader import PLAYER_LIST_ORDER
from datetime import datetime, timedelta
import random
import string
import json
import os
import re


class PlayerController:
    """Contrôleur de gestion des joueurs"""

    def __init__(self):
        self.view = MainView()

    def player_menu(self):
        """Menu de gestion des joueurs"""
        invalid_input = 0
        while True:
            if invalid_input == 0:
                self.view.clear_screen()
                self.view.display_menu("player")

            choice = self.view.user_prompts(21, ["", ""])

            if choice in ["1", "2", "3", "4"]:
                invalid_input = 0
                if choice == "1":
                    self.create_player()  # self.create_player()
                elif choice == "2":
                    self.edit_player()  # self.edit_player()
                elif choice == "3":
                    self.list_all_players()  # self.list_all_players()
                elif choice == "4":
                    break  # main menu

            else:  # invalid input
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

    def data_file_empty(self, file_name):
        """Returns bool"""
        if os.path.exists("data"):
            file_path = f'data/{file_name}.json'
        else:
            file_path = f'chess/data/{file_name}.json'

        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                self.view.notify_alert(31, ["", ""])
                return True

            if "players" not in data:
                self.view.notify_alert(32, ["", ""])
                return True
            else:
                return False

    def create_player(self):
        """Menu de creation de joueur"""
        self.view.new_header(5)
        player_id, first_name, last_name, birth_date = self.get_player_details("create")
        player = PlayerModel(player_id, first_name, last_name, birth_date)
        PlayerDataManager().save_new_player(player)
        self.view.notify_alert(2, ["", ""])
        self.view.user_prompts(0, ["", ""])

    def edit_player(self):
        """Menu d'edition de joueur"""
        file_name = "players"
        file_path = self.data_file_exists(file_name)
        if file_path[0]:
            if not self.data_file_empty(file_name):
                self.view.new_header(6)
                old_player = self.pick_a_player("edit", 1)
                if len(old_player) > 0:
                    op_id, op_first_name, op_last_name, op_birth_date = old_player
                    self.view.new_header(6)
                    self.view.notify_alert(30, [f'{op_id}, {op_first_name}', f'{op_last_name}, {op_birth_date}'])
                    new_player = self.get_player_details("edit")
                    np_id, np_first_name, np_last_name, np_birth_date = new_player
                    if any(var != "" for var in [np_id, np_first_name, np_last_name, np_birth_date]):
                        # mettre à jour uniquement les données modifiées
                        np_id = op_id if np_id == "" else np_id
                        np_first_name = op_first_name if np_first_name == "" else np_first_name
                        np_last_name = op_last_name if np_last_name == "" else np_last_name
                        np_birth_date = op_birth_date if np_birth_date == "" else np_birth_date
                        player = PlayerModel(np_id, np_first_name, np_last_name, np_birth_date)
                        if np_id == op_id:
                            PlayerDataManager().update_player(player)
                        else:
                            PlayerDataManager().replace_player(player, op_id)

                        self.view.notify_alert(4, ["", ""])
                    else:
                        self.view.notify_alert(29, ["", ""])
                        self.view.user_prompts(0, ["", ""])

            else:
                self.view.notify_alert(11, ["", ""])
                self.view.user_prompts(0, ["", ""])

        else:
            self.view.new_header(6)
            self.view.notify_alert(11, ["", ""])
            self.view.user_prompts(0, ["", ""])

    def pick_a_player_header(self, values, mode):
        if mode == "tournament":
            self.view.new_header(9)
            self.view.notify_alert(27, [values[0], values[1]])
        else:
            self.view.new_header(6)

        self.view.notify_alert(25, [values[2], values[3]])

    def pick_a_player(self, mode, number_of_players):
        """Returns a player list or a player's data"""
        players_list = PlayerDataManager().list_players(PLAYER_LIST_ORDER)
        page_size = 20
        total_players = len(players_list)
        total_pages = (total_players // page_size) + (1 if total_players % page_size != 0 else 0)
        tour_players = []

        for page in range(total_pages):
            if len(tour_players) < number_of_players:
                self.pick_a_player_header([len(tour_players), number_of_players, page + 1, total_pages], mode)
                start_index = page * page_size
                end_index = start_index + page_size
                page_data = players_list[start_index:end_index]
                self.view.display_table("pick_player", page_data)
                player_nbr = len(page_data)
                while True:
                    if mode == "edit":
                        values = [f"{player_nbr}]) de joueur à modifier"]
                    else:
                        values = [f"{player_nbr}]) de joueur à ajouter"]

                    if len(tour_players) < number_of_players:
                        if page + 1 == total_pages:
                            values.append("retourner au menu précédent")
                            bdd_player = str(self.view.user_prompts(27, values)).lower()
                        else:
                            values.append("passer à la page suivante")
                            bdd_player = str(self.view.user_prompts(27, values)).lower()

                    else:
                        break

                    if bdd_player == "":
                        break

                    else:
                        try:
                            bdd_player = int(bdd_player)
                            if 1 <= bdd_player <= player_nbr:  # comparer avec la liste des joueurs présents
                                player_data = page_data[bdd_player - 1]
                                chosen_player = list(player_data.values())
                                if mode == "edit":
                                    return chosen_player
                                else:
                                    if chosen_player in tour_players:
                                        self.view.notify_alert(26, ["", ""])
                                    else:
                                        tour_players.append(chosen_player)
                                        self.pick_a_player_header(
                                            [len(tour_players),
                                             number_of_players,
                                             page + 1,
                                             total_pages],
                                            mode)
                                        self.view.display_table("pick_player", page_data)

                        except ValueError:
                            self.view.invalid_input(16, [1, player_nbr])

        return tour_players

    def vali_date(self, date_input):
        """Returns date input normalisée, is_valid bool, notify_index int"""
        formats = [
            r"(\d{4})(\d{2})(\d{2})",
            r"(\d{4}) (\d{2}) (\d{2})",
            r"(\d{4})-(\d{2})-(\d{2})",
            r"(\d{4})\.(\d{2})\.(\d{2})",
            r"(\d{4}),(\d{2}),(\d{2})",
            r"(\d{4})/(\d{2})/(\d{2})",
            r"(\d{2})(\d{2})(\d{4})",
            r"(\d{2}) (\d{2}) (\d{4})",
            r"(\d{2})-(\d{2})-(\d{4})",
            r"(\d{2})\.(\d{2})\.(\d{4})",
            r"(\d{2}),(\d{2}),(\d{4})",
            r"(\d{2})/(\d{2})/(\d{4})"
        ]
        for fmt in formats:
            match = re.match(fmt, date_input)
            if match:
                groups = match.groups()
                if len(groups[0]) == 4:  # Format YYYY-MM-DD
                    year, month, day = map(int, groups)
                else:  # Format DD-MM-YYYY
                    day, month, year = map(int, groups)

                try:
                    birth_date = datetime(year, month, day)
                    today = datetime.now()
                    if birth_date > today:
                        return date_input, False, 3
                    age = today.year - birth_date.year - (
                        (today.month, today.day) < (birth_date.month, birth_date.day)
                    )
                    if age > 150:
                        return date_input, False, 4
                    elif age < 4:
                        return date_input, False, 5

                    return birth_date.strftime('%Y-%m-%d'), True, 0

                except ValueError:
                    return date_input, False, 3

        return date_input, False, 3

    def get_player_details(self, mode):
        """Returns player_id, first_name, last_name, birth_date"""
        if mode == "edit":
            self.view.notify_alert(28, ["", ""])

        player_id = self.player_id_prompt(mode)
        first_name = self.name_prompt(mode, 2)
        last_name = self.name_prompt(mode, 3)
        birth_date = self.birth_prompt(mode)

        return player_id, first_name, last_name, birth_date

    def player_id_prompt(self, mode):
        """Returns player_id"""
        while True:
            player_id = self.view.user_prompts(1, ["", ""]).upper()
            if re.match(r"[A-Z]{2}\d{5}", player_id) and len(player_id) == 7:
                if mode in ["create", "edit"]:
                    if not PlayerDataManager().id_exists(player_id):
                        break
                    else:
                        self.view.notify_alert(0, ["", ""])

                elif mode == "tournament":
                    break

            else:
                if mode == "edit":
                    if player_id == "":
                        break
                    else:
                        self.view.invalid_input(6, ["", ""])

                else:
                    self.view.invalid_input(6, ["", ""])

        return player_id

    def name_prompt(self, mode, index):
        """Returns player name"""
        while True:
            name = self.view.user_prompts(index, ["", ""])
            if name and name.replace("-", "").isalpha():
                break
            else:
                if mode == "edit":
                    if name == "":
                        break
                    else:
                        self.view.invalid_input(index - 1, ["", ""])

                else:
                    self.view.invalid_input(index - 1, ["", ""])

        return name

    def birth_prompt(self, mode):
        """Returns player birth date"""
        while True:
            birth_date = self.view.user_prompts(4, ["", ""])
            if mode != "edit":
                valid_date = self.vali_date(birth_date)
                if valid_date[1]:
                    birth_date = valid_date[0]
                    break
                else:
                    self.view.invalid_input(valid_date[2], ["", ""])

            else:
                if birth_date == "":
                    break
                else:
                    valid_date = self.vali_date(birth_date)
                    if valid_date[1]:
                        birth_date = valid_date[0]
                        break
                    else:
                        self.view.invalid_input(valid_date[2], ["", ""])

        return birth_date

    def generate_random_id(self):
        """Génère un ID au format XX#####"""
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=2))
            digits = ''.join(random.choices(string.digits, k=5))
            player_id = letters + digits
            if not PlayerDataManager().id_exists(player_id):
                return player_id

    def generate_random_date(self):
        """Génère une date aléatoire entre -8 et -120 ans"""
        current_year = datetime.now().year
        start_year = current_year - 120
        end_year = current_year - 8
        start_date = datetime(year=start_year, month=1, day=1)
        end_date = datetime(year=end_year, month=12, day=31)
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")

    def generate_random_players(self, number_of_players):
        """Returns list of players"""
        tournament_players = []
        file_path = self.data_file_exists("randomizer")
        if file_path[0]:
            with open(file_path[1], 'r', encoding='utf-8') as file:
                random_data = json.load(file)
                fr_names = random_data.get('noms_fr', None)
                en_names = random_data.get('noms_en', None)

            for n in range(number_of_players):
                player_id = self.generate_random_id()
                a = random.choice(["fr", "en"])
                if a == "fr":
                    prenom = random.choice(fr_names[0])
                    nom = random.choice(fr_names[1])
                else:
                    prenom = random.choice(en_names[0])
                    nom = random.choice(en_names[1])

                first_name = prenom
                last_name = nom
                birth_date = self.generate_random_date()
                new_player = [player_id, first_name, last_name, birth_date]
                tournament_players.append(new_player)

            return tournament_players

        else:
            self.view.notify_alert(8, [file_path, ""])
            self.view.user_prompts(0, ["", ""])
            return []

    def list_all_players(self):
        """Lists all players"""
        file_path = self.data_file_exists("players")
        if file_path[0]:
            ReportController().list_all_players()
        else:
            self.view.new_header(9)
            self.view.notify_alert(11, ['data/players.json', ""])
            self.view.user_prompts(0, ["", ""])
