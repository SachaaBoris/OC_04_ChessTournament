import os
from views.main import MainView
from tinydb import TinyDB, Query


class PlayerModel:
    """Model pour les joueurs"""

    def __init__(self, player_id, first_name, last_name, birth_date):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date
        }


class PlayerDataManager:
    """Data Management des joueurs"""

    def __init__(self):
        """Initialisation"""
        self.view = MainView()
        if os.path.exists("data"):
            db_path = 'data/players.json'
        else:
            db_path = 'chess/data/players.json'

        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            open(db_path, 'w').close()  # Create the file if it does not exist
        self.db = TinyDB(db_path)
        self.players_table = self.db.table('players')

    def id_exists(self, player_id):
        """Returns bool"""
        player_query = Query()
        return self.players_table.contains(player_query.player_id == player_id)

    def save_new_player(self, new_player):
        """Sauvegarder le nouveau joueur"""
        self.players_table.insert(new_player.to_dict())

    def update_player(self, edited_player):
        """Mettre à jour les nouvelles data joueur"""
        player_dict = edited_player.to_dict()
        player_id = player_dict['player_id']
        player_query = Query()
        self.players_table.update(player_dict, player_query.player_id == player_id)

    def replace_player(self, edited_player, old_id):
        """Remplacer les data d'un joueur"""
        player_dict = edited_player.to_dict()
        player_query = Query()
        self.players_table.update(player_dict, player_query.player_id == old_id)

    def save_player_list(self, players_list):
        """sauvegarder la liste de joueurs"""
        for player_data in players_list:
            player_id, first_name, last_name, birth_date = player_data
            player = PlayerModel(player_id, first_name, last_name, birth_date)
            if self.players_table.contains(Query().player_id == player_id):
                self.update_player(player)
            else:
                self.save_new_player(player)

    def list_players(self, order):
        """Retourne la liste des joueurs dans l'ordre alphabetique"""
        players_list = self.players_table.all()
        sorted_list = sorted(players_list, key=lambda x: x.get(order, "").lower())
        return sorted_list
