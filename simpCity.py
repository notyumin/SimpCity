from tabulate import tabulate
from operator import itemgetter
from re import sub
from colorama import init
from component_Logic import *
init()


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
