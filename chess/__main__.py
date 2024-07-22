from views.logo import ChessLogo
from controllers.main import MainController
from config_loader import FAVORITE_COLOR
import os.path
import os


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
    cmd = 'mode 130,35'
    os.system(cmd)
    cmd = f'color {FAVORITE_COLOR}'
    os.system(cmd)
    main()
