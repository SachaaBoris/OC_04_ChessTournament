import json
import os
from datetime import datetime

class Tournament:
    ''' Model pour les tournois '''
    
    def __init__(self, name, city, description, players, rounds, round, rounds_results, final_results, beg_date, end_date):
        self.name = name
        self.city = city
        self.desc = description
        self.players = players
        self.rounds = rounds
        self.round = 0
        self.rounds_results = []
        self.final_results = []
        self.beg_date = datetime.now().strftime("%Y-%m-%d_%H:%M")
        self.end_date = ""
    
    def to_dict(self):
        return {
            "tournament_name": self.name,
            "city": self.city,
            "description" : self.description,
            "players": self.players,
            "rounds": self.rounds,
            "round": self.round,
            "rounds_results": self.rounds_results,
            "final_results": self.final_results,
            "beg_date": self.beg_date,
            "end_date": self.end_date,
        }
    
    