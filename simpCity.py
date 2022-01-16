from random import randint
import pickle
from colorama import init

init()


def init_game():
    game_board = [
        # e.g. ['SHP','FAC','BCH','HWY']
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
    ]
    # Building name:count of buildings
    building_pool = {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8}
    return game_board, building_pool


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
    game_board = None
    building_pool = None

    while True:
        print("\nWelcome, mayor of Simp City!")
        print("----------------------------")
        print("\n1. Start new game")
        print("2. Load new game")
        print("\n0. Exit")

        option = input("Your choice? ")

        # Ensure inputted option is valid
        try:
            option = int(option)
            if option != 1 and option != 2 and option != 0:
                raise ValueError
        except ValueError:
            # print red warning using ANSI escape codes
            print("\033[91m{}\033[00m".format("Invalid option!"))
            continue

        if option == 1:
            game_board, building_pool = init_game()
            # Start game menu
            game_menu(game_board, building_pool)

        elif option == 2:
            game_board, building_pool = load_game("save.pickle")
            game_menu(game_board, building_pool)

        elif option == 0:
            print("Bye!")
            exit()


if __name__ == "__main__":
    main()
