from views.logo import ChessLogo
from controllers.main import MainController
import os.path


def main():
    ''' boot du programme '''

    if os.path.exists("data"):
        path = 'data/registered.json'
    else:
        path = 'chess/data/registered.json'

    if not os.path.isfile(path):
        ChessLogo().display_logo()  # YAGNI!

    try:
        main_controller = MainController()
        main_controller.main_menu()  # Main Menu
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


if __name__ == '__main__':
    ''' programme principal '''
    main()
