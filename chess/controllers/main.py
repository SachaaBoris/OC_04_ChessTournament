from views.main import MainView
from controllers.player import PlayerController
from controllers.tournament import TournamentController
from controllers.report import ReportController


class MainController:
    ''' Contrôleur principal '''

    def __init__(self):
        pass

    def main_menu(self):
        ''' menu principal du programme '''
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView().clear_screen()
                MainView().main_menu()
            
            choice = MainView().user_prompts(21, ["", ""])
            
            if choice in ["1", "2", "3", "4"]:
                invalid_input = 0
                if choice == "1":
                    PlayerController().player_menu()  # PlayerController().player_menu()
                elif choice == "2":
                    TournamentController().tournament_menu()  # TournamentController().tournament_menu()
                elif choice == "3":
                    ReportController().report_menu()  # ReportController().report_menu()
                elif choice == "4":
                    quit_app = MainView().quit_message()  # Quit
                    break
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0)
    