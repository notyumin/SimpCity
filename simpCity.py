from random import randint
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


def randomise_building(building_pool):
    building_1 = None
    building_2 = None

    total_buildings = 0
    for key in building_pool:
        total_buildings += building_pool[key]

    # Convert building pool and values to list
    building_categories = list(building_pool.keys())
    building_values = list(building_pool.values())

    if total_buildings == 0:
        # No buildings can be built
        pass
    elif total_buildings < 2:
        # Only one building can be built
        #  Obtain building category with only one building left
        building_1 = building_categories[building_values.index(1)]
    else:
        # Randomise and get 2 buildings
        while True:
            index = randint(0, 4)
            if building_values[index] > 0:
                # Decrement amount of building category
                building_values[index] -= 1
                # Set building for building 1/2
                if (building_1 == None):
                    building_1 = building_categories[index]
                elif (building_2 == None):
                    building_2 = building_categories[index]
                    break
    return [building_1, building_2]


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


if __name__ == "__main__":
    # main()
    randomise_building({"HSE": 0, "FAC": 0, "SHP": 0, "HWY": 0, "BCH": 1})
