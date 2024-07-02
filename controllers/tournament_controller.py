from views.views import MainView
from controllers import main_controller

class TournamentController:
    '''Contrôleur de gestion des tournois'''

    def __init__(self):
        pass
        
    def tournament_menu(self):
        invalid_input = 0
        while True:
            if invalid_input == 0:
                MainView.clear_screen()
                MainView().tournament_menu()
            
            choice = MainView().pick_option()

            if choice in ["1", "2", "3", "4"]:
                invalid_input = 0
                if choice == "1":  # self.create_tournament()
                    pass
                    # verifier si un pending tournament n'existe pas
                    # si pending_tournament exist, alors demande confirmation :
                    #sure = MainController.confirm_action()
                    #if sure:
                    #    PlayerController().player_menu()
                elif choice == "2":  # self.launch_tournament()
                    pass
                    # reprendre le pending tournament s'il y en a un
                    # sinon, renvoyer un message demandant de créer un tournoi
                elif choice == "3": # ReportController.list_tournaments()
                    pass
                elif choice == "4":  # main menu
                    break
            else:
                # Invalid input
                invalid_input = 1
                MainView().invalid_input(0)
