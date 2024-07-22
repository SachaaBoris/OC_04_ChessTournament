import os
from tinydb import TinyDB, Query


class Tournament:
    """Model pour les tournois"""

    def __init__(
            self, tournament_name, city, description, players, rounds, round,
            rounds_results, final_results, beg_date, end_date):
        """Initialisation"""
        self.tournament_name = tournament_name
        self.city = city
        self.description = description
        self.players = players
        self.rounds = rounds
        self.round = round
        self.rounds_results = rounds_results
        self.final_results = final_results
        self.beg_date = beg_date
        self.end_date = end_date

    def to_dict(self):
        """Ajoute au dictionnaire"""
        return {
            "tournament_name": self.tournament_name,
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
    """Data Management du tournoi"""

    def __init__(self):
        """Initialisation"""
        if os.path.exists("data"):
            db_path = 'data/tournaments.json'
        else:
            db_path = 'chess/data/tournaments.json'

        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.db = TinyDB(db_path)
        self.tournament_table = self.db.table('tournaments')

    def initialize_tournament_dict(self, data):
        """Initialise le tournoi depuis un dictionnaire"""
        tournament = Tournament(
            tournament_name=data['tournament_name'],
            city=data['city'],
            description=data['description'],
            players=data['players'],
            rounds=data['rounds'],
            round=data['round'],
            rounds_results=data['rounds_results'],
            final_results=data['final_results'],
            beg_date=data['beg_date'],
            end_date=data['end_date']
        )
        return tournament

    def initialize_tournament_list(self, data):
        """Initialise le tournoi depuis une liste"""
        tournament = Tournament(
            tournament_name=data[0],
            city=data[1],
            description=data[2],
            players=data[3],
            rounds=data[4],
            round=data[5],
            rounds_results=data[6],
            final_results=data[7],
            beg_date=data[8],
            end_date=data[9]
        )
        return tournament

    def save_new_tournament(self, tournament):
        """Sauvegarder le nouveau tournoi"""
        tournament_dict = tournament.to_dict()
        self.tournament_table.insert(tournament_dict)

    def update_tournament(self, tournament):
        """Mettre à jour les data du tournoi"""
        if not isinstance(tournament, Tournament):
            tournament = self.initialize_tournament(tournament)

        tournament_dict = tournament.to_dict()

        self.tournament_table.update(
            tournament_dict,
            self.matching_tournament(tournament)
        )

    def matching_tournament(self, tournament):
        """Compare les tournois indépendamment de l'ordre des joueurs"""
        tournament_players_set = set(tuple(player) for player in tournament.players)

        def _matching(t):  # fonction interne
            return (
                t['tournament_name'] == tournament.tournament_name and
                t['city'] == tournament.city and
                t['description'] == tournament.description and
                set(tuple(player) for player in t['players']) == tournament_players_set and
                t['rounds'] == tournament.rounds
            )

        return _matching

    def has_tournament_started(self):
        """Returns bool"""
        existing_tournament = Query()
        pending_tournament = self.tournament_table.search(existing_tournament.beg_date != "")

        if pending_tournament:
            return True
        return False

    def list_tournaments(self):
        """Returns tournament dictionnary list"""
        return self.tournament_table.all()

    def id_exists(self, player_id):
        """Returns bool"""
        player_query = Query()
        return self.players_table.contains(player_query.player_id == player_id)

    def list_players(self):
        """Returns players dictionnary list"""
        return self.players_table.all()

    def get_tournament_data(self):
        """Returns dictionnary"""
        return self.tournament_table.all()
