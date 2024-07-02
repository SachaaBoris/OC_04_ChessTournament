import json
import os

class PlayerModel:
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

    @staticmethod
    def save_new_player(new_player):
        file_path = 'data/players.json'
        # Vérifier si le fichier existe
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"players": []}
        
        data["players"].append(new_player.to_dict())
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def id_exists(player_id):
        file_path = 'data/players.json'
        if not os.path.isfile(file_path):
            return False

        with open(file_path, 'r') as f:
            data = json.load(f)

        return any(player["player_id"] == player_id for player in data.get("players", []))

    @classmethod
    def from_dict(cls, data):
        return cls(data["player_id"], data["first_name"], data["last_name"], data["birth_date"])