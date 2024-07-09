from views.logo import ChessLogo
from controllers.main import MainController
import os.path

def main():
    if os.path.exists("data"):
        path='data/registered.json'
    else:
        path='chess/data/registered.json'
        
    if not os.path.isfile(path):
        displayLogo = ChessLogo().display_logo()
    
    try:
        main_controller = MainController()
        main_controller.main_menu()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

# Programme principal
if __name__ == '__main__':
    main()
