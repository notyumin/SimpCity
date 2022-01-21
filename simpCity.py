from random import randint
import pickle
from re import sub
from colorama import init
from tabulate import tabulate
from operator import itemgetter

# UI for in-game menu
def game_menu(game_board, building_pool):
    turn_counter = 1
    while True:
        reply = isFull(game_board)
        if reply is True:
            endgame(game_board, building_pool)
            break

        # Print turn and game board
        print("\nTurn " + str(turn_counter))
        print_game(game_board, building_pool)

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
                turn_counter += 1
                break
        elif option == 3:
            continue
        elif option == 4:
            calculate_score(game_board)
        elif option == 5:
            save_file(game_board, building_pool, "save.pickle")
            return
        elif option == 0:
            print("Returning to main menu...")
            return
    return


# Function to load file for game and highscore
def load_file(filename):
    pickle_in = open(filename, "rb")
    items = pickle.load(pickle_in)
    item1 = items[0]
    if len(items) == 2:
        item2 = items[1]
    return (item1, item2)


# Function to save file for game and highscore
def save_file(item1, item2, filename):
    pickle_out = open(filename, "wb")
    pickle.dump([item1, item2], pickle_out)
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
    bList = []
    header = f"    "
    # Get column length of board and write header
    for i in range(len(board[0])):
        header += f"{chr(65+i):<6}"
    bList.append(header)

    row_count = 1
    for row in board:
        col_separator = " +" + (len(board[0]) * "-----+")
        bList.append(col_separator)
        #  Prints out contents of row center aligned and with a width of 5
        row_content = f"{row_count}|"
        for col in row:
            row_content += f"{col:^5}|"
        bList.append(row_content)
        row_count += 1
    bList.append(col_separator)
    return bList


def print_remaining_buildings(building_pool):
    data = []
    pList = []
    for pair in building_pool.items():
        data.append(pair)
    list = tabulate(data, headers=["Building", "Remaining"])
    for line in list.splitlines():
        pList.append(line)
    return pList


def print_game(game_board, building_pool):
    a = print_board(game_board)
    b = print_remaining_buildings(building_pool)
    if len(a) > len(b):
        for i in range(len(a) - len(b)):
            b.append("")
        res = "\n".join("{} {:>35}".format(x, y) for x, y in zip(a, b))
        print(res + "\n")


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
    board = [["" for a in range(size)] for b in range(size)]
    return board


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


# check game board full
def isFull(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "":
                return False
    return True


# end game
def endgame(board, pool):
    print("\nFinal layout of Simp City:")
    print_game(board, pool)
    score = calculate_score(board)
    filename = "high" + str(len(board)) + ".pickle"
    high, ignore = load_file(filename)
    p = 0
    while p in range(len(high)):
        if score > high[p][1]:
            position = p + 1
            print(
                "Congratulations! You made the high score board at position "
                + str(position)
                + "!"
            )
            name = str(input("Please enter your name (max 20 chars): "))
            high.append((name, score))
            high = sorted(high, key=itemgetter(1), reverse=True)[:10]
            save_file(high, None, filename)
            print_highscores(high)
            return
        p += 1
    return


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
                # HSE is scored based on items around it
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
                # SHP is scored based on unique items around it
                item_above, item_below, item_right, item_left = get_items_around(
                    game_board, i, y
                )
                sub_total = 0
                # Checks the items around
                unique_buildings = ["BCH", "FAC", "HSE", "HWY", "MON", "PRK"]
                for item in [item_above, item_below, item_right, item_left]:
                    if item in unique_buildings:
                        sub_total += 1
                        # remove unique building from pool so that it can't be scored again
                        unique_buildings.remove(item)
                SHP_scores.append(sub_total)

            elif curr_item == "HWY":
                x = 0
                # Each individual highway gets scored based on how long the highway is
                length = 1

                # Checks right & left of current item and adds to length of highway
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
                # Park is scored based on the size. Crosscheck with score dictionary. Max size of scoring for a park is 8
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
                    # Append corner monument score
                    MON_scores.append(2)
                else:
                    # Append normal monument score
                    MON_scores.append(1)

    # FAC scores 1pt/FAC up to  a maximum of 4pts/FAC.
    FAC_scores = [min(factory_count, 4) if i < 4 else 1 for i in range(factory_count)]

    # Monuments get scored normally unless there are 3 corner-built monuments
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
        building_type_scores[i] = [
            score for score in building_type_scores[i] if score != 0
        ]
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
    print("\nTotal score: " + str(total_score))
    return total_score


# Obtains coordinates of any chunk of vertically & horizontally connected PRK items
def crawl_parks(game_board, i, y, park_coords):
    item_above, item_below, item_right, item_left = get_items_around(game_board, i, y)
    coords = (i, y)
    # append current coordinates to park coords
    park_coords.append(coords)

    # Check according to ↓, →, ↑, ←
    # Traversed items are stored in park_coords
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


# UI to choose which highscore to view
def highscores_menu():
    size = None
    while True:
        print("\nChoose which High Score to view:")
        print("\n1. 4x4 High Score")
        print("2. 5x5 High Score")
        print("3. 6x6 High Score")
        print("4. 7x7 High Score")
        print("\n0. Back to Main Menu")

        option = int(input("Your choice? "))
        size = option + 3
        try:
            if (
                option != 1
                and option != 2
                and option != 3
                and option != 4
                and option != 0
            ):
                raise ValueError
        except ValueError:
            # print red warning using ANSI escape codes
            print("\033[91m{}\033[00m".format("Invalid option!"))
            continue

        if option == 0:
            return

        else:
            filename = "high" + str(size) + ".pickle"
            high, ignore = load_file(filename)
            print_highscores(high)


def print_highscores(high):
    print("---------------  HIGH SCORES  ---------------")
    print("Pos " + f'{"Player": <35} Score')
    print("--- " + f'{"------": <35} -----')
    num = 1
    for i in high:
        no = str(num) + "."
        print("{:>3} {:<38} {:0}".format(no, *i))
        num += 1
    print("---------------------------------------------")
    return


def get_items_around(game_board, i, y):
    # obtains items around a given coordinate.
    # Returns none for an item if it's out-of-bounds
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


def main():
    size = None
    buildings = None

    while True:
        print("\nWelcome, mayor of Simp City!")
        print("----------------------------")
        print("\n1. Start new game")
        print("2. Load saved game")
        print("3. Show High Scores")
        print("4. Options")
        print("\n0. Exit")
        option = input("Your choice? ")
        # if wanna edit pickle, it is here
        # score = [("Never", 56), ("Gonna", 53), ("Give", 52), ("You", 52), ("Up", 51), ("Never", 51), ("Gonna", 50), ("Let", 49), ("You", 49), ("Down", 48)]
        # save_file(score,None,"high4.pickle")

        # Ensure inputted option is valid
        try:
            option = int(option)
            if (
                option != 1
                and option != 2
                and option != 3
                and option != 4
                and option != 0
            ):
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
            game_board, building_pool = load_file("save.pickle")
            if game_board and building_pool is None:
                print("\033[91m{}\033[00m".format("No game saved!"))
            else:
                game_menu(game_board, building_pool)

        elif option == 3:
            highscores_menu()

        elif option == 4:
            size, buildings = option_menu()

        elif option == 0:
            print("Bye!")
            exit()


if __name__ == "__main__":
    main()
