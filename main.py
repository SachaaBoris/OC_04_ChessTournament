from views.logo import ChessLogo
from controllers import main_controller
import os.path

# Programme principal
if __name__ == '__main__':
    
    if not os.path.isfile('data/registered.json'):
        displayLogo = ChessLogo().display_logo()
    
    try:
        main_controller = main_controller.MainController()
        main_controller.main_menu()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise