# initial commit
print("Welcome, mayor of Simp City")
print("----------------------------")


def init_game():
    game_board = [
        # e.g. ['SHP','FAC','BCH','HWY']
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
    ]
    # Building name:count of buildings
    building_pool = {
        "HSE": 8,
        "FAC": 8,
        "SHP": 8,
        "HWY": 8,
        "BCH": 8
    }
    return game_board, building_pool


def game_menu(game_board, building_pool):
    print("This is the game menu...")
    return


def load_game():
    # implementation
    return


def main():
    game_board = None
    building_pool = None

    while True:
        print("\n1. Start new game")
        print("2. Load new game")
        print("\n0. Exit")

        option = input("Your choice? :")

        # Ensure inputted option is valid
        try:
            option = int(option)
            if (option != 1 and option != 2 and option != 0):
                raise ValueError
        except ValueError:
            # print red warning using ANSI escape codes
            print("\033[91m{}\033[00m".format("Invalid option!"))
            continue

        if option == 1:
            if (game_board == None or building_pool == None):
                # Get blank game board and default building pool
                game_board, building_pool = init_game()
            # Start game menu
            game_menu(game_board, building_pool)

        elif option == 2:
            load_game()

        elif option == 0:
            print("Bye!")
            exit()


main()
