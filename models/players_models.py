import json
import os

class PlayerModel:
    ''' Model pour les joueurs '''
    
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

    def list_players():
        file_path = 'data/players.json'
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get("players", [])
        else:
            return []

    @staticmethod
    def save_new_player(new_player):
        file_path = 'data/players.json'
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"players": []}
        
        data["players"].append(new_player.to_dict())
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def update_player(edited_player):
        file_path = 'data/players.json'
        player_id = edited_player.player_id
        
        # Vérifier si le fichier existe
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"players": []}
        
        found = False
        for i, player in enumerate(data["players"]):
            if player.get('player_id') == player_id:
                data["players"][i] = edited_player.to_dict()
                found = True
                break
        
        if found:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
    
    @staticmethod
    def save_player_list(players_list):
        file_path = 'data/players.json'
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"players": []}
        
        existing_players = {player["player_id"]: player for player in data.get("players", [])}

        # Convertir la liste en dictionnaire
        for player_data in players_list:
            if len(player_data) == 4:
                player_dict = {
                    "player_id": player_data[0],
                    "first_name": player_data[1],
                    "last_name": player_data[2],
                    "birth_date": player_data[3]
                }
                existing_players[player_dict["player_id"]] = player_dict
        
        data["players"] = list(existing_players.values())
        
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
        