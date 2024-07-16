from views.main import MainView


class ChessLogo:
    def display_logo(self):
        MainView.clear_screen()
        chess_logo = [
            " ",
            "                   CHESS TOURNAMENT MANAGER",
            "                            v0.1",
            " ",
            "                            &@@@(",
            "                          @@@@@@@@@",
            "                       &@@@@@@ @@@@@@#",
            "                     @@@@@@@    /@@@@@@@",
            "      @@@         &@@@@@@@@##  ,##@@@@@@@@&         @@@",
            "   *@@@@@@@(    @@@@@@@@@@@&     @@@@@@@@@@@@    #@@@@@@@",
            "  @@@@@@@@@@@ @@@@@@@@@@@@@@,   #@@@@@@@@@@@@@@.@@@@@@@@@@@",
            "    #@@@@@&     *@@@@@@@@@@#    *%@@@@@@@@@@,     &@@@@@/",
            "       @           @@@@@@@@@@   @@@@@@@@@@           @",
            "     /@@@#       ,@@@@@@@@@@@   &@@@@@@@@@@.       %@@@*",
            "   @@@@@@@@@   @@@@@@@@@@@@@,   %@@@@@@@@@@@@@   @@@@@@@@@",
            "  /@@@@@@@@@# .@@@@@@@@@@@@@     @@@@@@@@@@@@@  %@@@@@@@@@,",
            "     @@@@@       @@@@@@@@@/       %@@@@@@@@&       @@@@@",
            "       .           .@@@@@           @@@@@            .",
            "                      @@@@&&&&&&&&&@@@%",
            "                         @@@@@@@@@@@",
            "                           @@@@@@#",
            "                              @",
            " ",
            " ",
            "                    Entrée pour continuer"
        ]
        for line in chess_logo:
            print(f"{line}")

        return input(" ")
