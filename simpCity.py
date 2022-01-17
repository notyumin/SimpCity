from random import randint
import pickle
from re import sub
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
            calculate_score(game_board)
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


def calculate_score(game_board):
    factory_count = 0
    monument_count = 0
    monument_corner_count = 0

    BCH_scores = []
    HSE_scores = []
    SHP_scores = []
    HWY_scores = []
    PRK_scores = []
    MON_scores = []

    PRK_score_dict = {1: 1, 2: 3, 3: 8, 4: 16, 5: 22, 6: 23, 7: 24, 8: 25}

    coordinate_blacklist = []

    for i in range(0, len(game_board)):
        for y in range(0, len(game_board)):
            if (i, y) in coordinate_blacklist:
                # Skip coord
                continue

            curr_item = game_board[i][y]
            if curr_item == "BCH":
                # Beaches get bonus points for being built in col A/D
                if y == 0 or y == 3:
                    BCH_scores.append(3)
                else:
                    BCH_scores.append(1)

            elif curr_item == "FAC":
                # Factory score is calculated last, after getting total number of factories
                factory_count += 1

            elif curr_item == "HSE":
                item_above, item_below, item_right, item_left = get_items_around(
                    game_board, i, y
                )
                sub_total = 0
                for item in [item_above, item_below, item_right, item_left]:
                    if item == "FAC":
                        HSE_scores.append(1)
                        sub_total = 0
                        break
                    elif item == "HSE" or item == "SHP":
                        sub_total += 1
                    elif item == "BCH":
                        sub_total += 2
                HSE_scores.append(sub_total)

            elif curr_item == "SHP":
                item_above, item_below, item_right, item_left = get_items_around(
                    game_board, i, y
                )
                sub_total = 0
                unique_buildings = ["BCH", "FAC", "HSE", "HWY"]
                for item in [item_above, item_below, item_right, item_left]:
                    if item in unique_buildings:
                        sub_total += 1
                        unique_buildings.remove(item)
                SHP_scores.append(sub_total)

            elif curr_item == "HWY":
                x = 0
                # Each individual highway gets scored based on how long the highway is
                length = 1
                while True:
                    item_right = get_items_around(game_board, i, y + x)[2]
                    x += 1
                    if item_right == "HWY":
                        length += 1
                    else:
                        break
                x = 0
                while True:
                    item_left = get_items_around(game_board, i, y - x)[3]
                    x += 1
                    if item_left == "HWY":
                        length += 1
                    else:
                        break
                HWY_scores.append(length)

            elif curr_item == "PRK":
                current_park = crawl_parks(game_board, i, y, [])
                PRK_scores.append(PRK_score_dict[min(len(current_park), 8)])
                # Add park to coordinate blacklist - don't need to traverse again
                coordinate_blacklist.extend(current_park)

            elif curr_item == "MON":
                monument_count += 1

                # bools to check if item is in corner
                is_bottom_corner = i + 1 > (len(game_board) - 1)
                is_right_corner = y + 1 > (len(game_board[0]) - 1)
                is_top_corner = i - 1 < 0
                is_left_corner = y - 1 < 0
                corner_checks = [
                    is_right_corner,
                    is_bottom_corner,
                    is_left_corner,
                    is_top_corner,
                ]

                # For an item to  be in a corner, exactly 2 of the checks must eval to true
                if corner_checks.count(True) == 2:
                    monument_corner_count += 1
                    MON_scores.append(2)
                else:
                    MON_scores.append(1)

    # FAC scores 1pt/FAC up to  a maximum of 4pts/FAC
    FAC_scores = [min(factory_count, 4) for i in range(factory_count)]

    # MON
    if monument_corner_count >= 3:
        # Override monument score
        MON_scores = [4 for i in range(monument_count)]

    total_score = 0
    i = 0
    building_type_scores = [
        BCH_scores,
        HSE_scores,
        SHP_scores,
        HWY_scores,
        FAC_scores,
        MON_scores,
        PRK_scores,
    ]
    while i < len(building_type_scores):
        if len(building_type_scores[i]) != 0:
            name = ""
            if i == 0:
                name = "BCH"
            elif i == 1:
                name = "HSE"
            elif i == 2:
                name = "SHP"
            elif i == 3:
                name = "HWY"
            elif i == 4:
                name = "FAC"
            elif i == 5:
                name = "MON"
            elif i == 6:
                name = "PRK"
            subtotal = sum(building_type_scores[i])
            subtotal_text = (
                name
                + ": "
                + " + ".join("{0}".format(score) for score in building_type_scores[i])
            )
            print(subtotal_text + " = " + str(subtotal))
            total_score += subtotal
        i += 1

    return total_score


def crawl_parks(game_board, i, y, park_coords):
    item_above, item_below, item_right, item_left = get_items_around(game_board, i, y)
    coords = (i, y)
    park_coords.append(coords)

    if item_below == "PRK" and (i + 1, y) not in park_coords:
        park_coords = crawl_parks(game_board, i + 1, y, park_coords)

    if item_right == "PRK" and (i, y + 1) not in park_coords:
        park_coords = crawl_parks(game_board, i, y + 1, park_coords)

    if item_above == "PRK" and (i - 1, y) not in park_coords:
        park_coords = crawl_parks(game_board, i - 1, y, park_coords)

    if item_left == "PRK" and (i, y - 1) not in park_coords:
        park_coords = crawl_parks(game_board, i, y - 1, park_coords)

    # Base case - item's surroundings are already crawled through or are not parks
    return park_coords


def get_items_around(game_board, i, y):
    try:
        if (i - 1) >= 0:
            item_above = game_board[i - 1][y]
        else:
            item_above = None
    except IndexError:
        item_above = None
    try:
        item_below = game_board[i + 1][y]
    except IndexError:
        item_below = None
    try:
        item_right = game_board[i][y + 1]
    except IndexError:
        item_right = None
    try:
        if (y - 1) >= 0:
            item_left = game_board[i][y - 1]
        else:
            item_left = None
    except IndexError:
        item_left = None
    return item_above, item_below, item_right, item_left


if __name__ == "__main__":
    main()
