import os
import shutil
import time
from tinydb import TinyDB, Query


class Tournament:
    """ Model pour les tournois """
    
    def __init__(self, name, city, description, players, rounds, round,
                 rounds_results, final_results, beg_date, end_date):
        self.name = name
        self.city = city
        self.description = description
        self.players = players
        self.rounds = rounds
        self.round = 0
        self.rounds_results = []
        self.final_results = []
        self.beg_date = ""
        self.end_date = ""
    
    def to_dict(self):
        return {
            "tournament_name": self.name,
            "city": self.city,
            "description": self.description,
            "players": self.players,
            "rounds": self.rounds,
            "round": self.round,
            "rounds_results": self.rounds_results,
            "final_results": self.final_results,
            "beg_date": self.beg_date,
            "end_date": self.end_date,
        }


class TournamentDataManager:
    """ Data Management du tournoi """
    
    def __init__(self):
        if os.path.exists("data"):
            db_path = 'data/pending_tournament.json'
        else:
            db_path = 'chess/data/pending_tournament.json'
        
        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.db = TinyDB(db_path)
        self.tournament_table = self.db.table('tournament')
    
    def to_dict(self, tournament_data):
        """ returns dictionnary """
        return {
            "tournament_name": tournament_data[0],
            "city": tournament_data[1],
            "description": tournament_data[2],
            "players": tournament_data[3],
            "rounds": tournament_data[4],
            "round": tournament_data[5],
            "rounds_results": tournament_data[6],
            "final_results": tournament_data[7],
            "beg_date": tournament_data[8],
            "end_date": tournament_data[9]
        }
    
    def save_new_tournament(self, tournament_data):
        """ sauvegarder le nouveau tournoi """
        tournament_dict = self.to_dict(tournament_data)
        self.tournament_table.insert(tournament_dict)
    
    def has_tournament_started(self):
        """ returns bool """
        existing_tournament = Query()
        pending_tournament = self.tournament_table.search(existing_tournament.beg_date != "")
        
        if pending_tournament:
            return True
        return False
    
    def update_tournament(self, tournament_data):
        """ mettre à jour les data du tournoi """
        tournament_dict = self.to_dict(tournament_data)
        existing_tournament = Query()
        
        with TinyDB(self.db_path) as db:
            tournament_table = db.table('tournament')
            tournament_table.update(tournament_dict, existing_tournament.tournament_name == tournament_data[0])
    
    def close_tournament(self, city, end_date):
        """ renomme et déplace le pending_tournement """
        self.db.close()
        city = city.replace(", ", "-")
        filename = f"tournament_{end_date.split('_')[0]}_{city}.json"
        if os.path.exists("data"):
            old_path = 'data/pending_tournament.json'
        else:
            old_path = 'chess/data/pending_tournament.json'
        old_path = 'data/pending_tournament.json'
        new_path = os.path.join('data', 'tournaments', filename)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.move(old_path, new_path)
        
    def list_tournaments(self):
        """ returns dictionnary """
        return self.tournament_table.all()
    
    def id_exists(self, player_id):
        """ returns bool """
        player_query = Query()
        return self.players_table.contains(player_query.player_id == player_id)
    
    def list_players(self):
        """ returns dictionnary """
        return self.players_table.all()
    
    def get_tournament_data(self):
        """ returns dictionnary """
        return self.tournament_table.all()
    