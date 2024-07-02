from views.views import MainView
from controllers import main_controller

class ReportController:
    '''Contrôleur de gestion des rapports'''

    def __init__(self):
        pass

    def report_menu(self):
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView.clear_screen()
                MainView().report_menu()
            
            choice = MainView().pick_option()
            
            if choice in ["1", "2", "3" ,"4" ,"5" ,"6"]:
                invalid_input = 0
                if choice == "1":  # self.list_players()
                    pass
                elif choice == "2":  # self.list_tournaments()
                    pass
                elif choice == "3":  # self.get_tournament_info()
                    pass
                elif choice == "4":  # self.get_tournament_players()
                    pass
                elif choice == "5":  # self.get_tournament_matches()
                    pass
                elif choice == "6":  # main menu
                    break
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0)
