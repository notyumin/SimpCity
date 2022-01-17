from random import randint
import pickle
from colorama import init

# UI for in-game menu
def game_menu(game_board, building_pool):
    turn_counter = 1
    while True:
        # Print turn and game   board
        print("\nTurn " + str(turn_counter))
        print_board(game_board)

        # Get randomised building
        buildings = randomise_building(building_pool)

        # Print options for turn
        print("1. Build a " + buildings[0])
        print("2. Build a " + buildings[1])
        print("3. See remaining buildings")
        print("4. See current score\n")
        print("5. Save game")
        print("0. Exit to main menu")
        print("Your choice?")
        option = input()

        turn_counter += 1
        # Ensure inputted option is valid
        try:
            option = int(option)
            if (
                option != 1
                and option != 2
                and option != 3
                and option != 4
                and option != 5
                and option != 0
            ):
                raise ValueError
        except ValueError:
            print("\033[91m{}\033[00m".format("Invalid option!"))
            continue

        if option == 1 or option == 2:
            while True:
                column = input("Column :")
                row = input("Row :")
                if option == 1:
                    to_be_built = buildings[0]
                elif option == 2:
                    to_be_built = buildings[1]
                try:
                    game_board = build(game_board, column, row, to_be_built)
                except ValueError as error:
                    print("\033[91m{}\033[00m".format(error))
                    # Start loop from top & make user input again
                    continue
                building_pool[to_be_built] -= 1
                break
        elif option == 3:
            continue
        elif option == 4:
            continue
        elif option == 5:
            save_game(game_board, building_pool, "save.pickle")
        elif option == 0:
            print("Returning to main menu...")
            return
    return


# Function to load game data
def load_game(filename):
    pickle_in = open(filename, "rb")
    board = pickle.load(pickle_in)
    game = board[0]
    pool = board[1]
    return (game, pool)


# Function to save game data
def save_game(board, pool, filename):
    pickle_out = open(filename, "wb")
    pickle.dump([board, pool], pickle_out)
    pickle_out.close()


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
                if building_1 == None:
                    building_1 = building_categories[index]
                elif building_2 == None:
                    building_2 = building_categories[index]
                    break
    return [building_1, building_2]


def print_board(board):
    header = f"    "
    # Get column length of board and write header
    for i in range(len(board[0])):
        header += f"{chr(65+i):<6}"
    print(header)

    row_count = 1
    for row in board:
        col_separator = " +" + (len(board[0]) * "-----+")
        print(col_separator)
        #  Prints out contents of row center aligned and with a width of 5
        row_content = f"{row_count}|"
        for col in row:
            row_content += f"{col:^5}|"
        print(row_content)
        row_count += 1
    print(col_separator)
    return


# UI to choose city size/building pool
def option_menu():
    buildings = None
    size = None
    while True:
        print("\n1. Choose Building Pool")
        print("2. Choose City Size")
        print("\n0. Back to Main Menu")

        option = int(input("Your choice? "))
        try:
            if option != 1 and option != 2 and option != 0:
                raise ValueError
        except ValueError:
            # print red warning using ANSI escape codes
            print("\033[91m{}\033[00m".format("Invalid option!"))
            continue

        if option == 1:
            buildings = choose_building()

        elif option == 2:
            size = choose_citysize()

        elif option == 0:
            return size, buildings


# UI to choose citysize menu
def choose_citysize():
    print("\nCity Size available in the SimpCity: ")
    print("\n1. 4x4")
    print("2. 5x5")
    print("3. 6x6")
    print("4. 7x7")
    print("\n0. Back to Options Menu")

    option = int(input("Your choice? "))
    try:
        if option > 4 or option < 0:
            raise ValueError
    except ValueError:
        # print red warning using ANSI escape codes
        print("\033[91m{}\033[00m".format("Invalid option!"))
        return
    if option == 0:
        return
    else:
        size = option + 3
        return size


# UI to choose building pool
def choose_building():
    print("\nBuildings in the SimpCity: ")
    print("\nHouse (HSE)")
    print("Factory (FAC)")
    print("Shop (SHP)")
    print("Highway (HWY)")
    print("Beach (BCH)")
    print("Park (PRK)")
    print("Monument (MON)")
    print(
        "\nChoose 5 buildings from the list. Separate each building's abbreviations with a comma and space!\nAbbreviations should be all CAPS"
    )
    print("eg: HSE, FAC, SHP, HWY, BCH")
    buildings = input("\nChoosen Building Pool:").split(", ")

    # input not 5 buildings
    try:
        if len(buildings) != 5:
            raise ValueError
    except ValueError:
        # print red warning using ANSI escape codes
        print("\033[91m{}\033[00m".format("Invalid option! Should be 5 buildings"))
        return

    # input not in building list
    try:
        for i in buildings:
            if i not in ["HSE", "FAC", "SHP", "HWY", "BCH", "PRK", "MON"]:
                raise ValueError
    except ValueError:
        # print red warning using ANSI escape codes
        print("\033[91m{}\033[00m".format("Invalid Building!"))
        return

    # input duplicate buildings
    try:
        if len(buildings) != len(set(buildings)):
            raise ValueError
    except ValueError:
        # print red warning using ANSI escape codes
        print("\033[91m{}\033[00m".format("Duplicate Buildings!"))
        return
    return buildings


# build chosen city size
def build_grid(size):
    try:
        if size > 7 or size < 4:
            raise ValueError
    except ValueError:
        # print red warning using ANSI escape codes
        print("\033[91m{}\033[00m".format("Invalid dimension!"))
        return
    given_value = ""
    column = []
    row = []
    column.extend([given_value for i in range(size)])
    row.extend([column for i in range(size)])
    return row


# build building pool
def build_pool(buildings, size):
    if size is None:
        size = 4
    building_pool = {}
    num = int(((size * size) / 16) * 8)
    for i in buildings:
        building_pool[i] = num
    return building_pool


# finalize user's choice
def set_game(size, buildings):
    if buildings is None and size is None:
        size = 4
        default_pool = ["HSE", "FAC", "SHP", "HWY", "BCH"]
        game_board = build_grid(size)
        building_pool = build_pool(default_pool, size)
        return game_board, building_pool
    elif size is None:
        size = 4
        game_board = build_grid(size)
        building_pool = build_pool(buildings, size)
        return game_board, building_pool

    elif buildings is None:
        game_board = build_grid(size)
        default_pool = ["HSE", "FAC", "SHP", "HWY", "BCH"]
        building_pool = build_pool(default_pool, size)
        return game_board, building_pool

    else:
        game_board = build_grid(size)
        building_pool = build_pool(buildings, size)
        return game_board, building_pool

def build(board, column, row, building):
    # Obtains index from  letter by getting unicode value of letter
    try:
        column_index = ord(column.lower()) - 97
    except:
        raise ValueError("Invalid column value!")
    else:
        if column_index < 0 or column_index > 25:
            raise ValueError("Invalid column value!")

    try:
        row_index = int(row) - 1
    except ValueError as error:
        raise
    else:
        if row_index > len(board[0]) or column_index > len(board):
            raise ValueError("Invalid row/column value!")

    # Set building in board
    if board[row_index][column_index] == "":
        board[row_index][column_index] = building
    else:
        raise ValueError("Invalid placement - block not empty")

    return board


def main():
    size = None
    buildings = None

    while True:
        print("\nWelcome, mayor of Simp City!")
        print("----------------------------")
        print("\n1. Start new game")
        print("2. Load new game")
        print("3. Options")
        print("\n0. Exit")

        option = input("Your choice? ")

        # Ensure inputted option is valid
        try:
            option = int(option)
            if option != 1 and option != 2 and option != 3 and option != 0:
                raise ValueError
        except ValueError:
            # print red warning using ANSI escape codes
            print("\033[91m{}\033[00m".format("Invalid option!"))
            continue

        if option == 1:
            game_board, building_pool = set_game(size, buildings)
            # Start game menu
            game_menu(game_board, building_pool)

        elif option == 2:
            game_board, building_pool = load_game("save.pickle")
            game_menu(game_board, building_pool)

        elif option == 3:
            size, buildings = option_menu()

        elif option == 0:
            print("Bye!")
            exit()


if __name__ == "__main__":
    main()
