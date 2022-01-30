import pickle
from random import randint


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
                if building_1 is None:
                    building_1 = building_categories[index]
                elif building_2 is None:
                    building_2 = building_categories[index]
                    break
    return [building_1, building_2]


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
    except ValueError:
        raise ValueError("Invalid column value!")
    else:
        if column_index < 0 or column_index > 25:
            raise ValueError("Invalid column value!")

    try:
        row_index = int(row) - 1
    except ValueError as error:
        raise error
    else:
        if row_index > len(board[0]) or column_index > len(board):
            raise ValueError("Invalid row/column value!")

    # Set building in board
    if board[row_index][column_index] != "":
        raise ValueError("Invalid placement - block not empty")

    # check if is orthogonal to other buildings
    available_spots = get_buildable(board)
    if (row_index, column_index) not in available_spots:
        raise ValueError("Must be orthogonally adjacent to other buildings!")

    board[row_index][column_index] = building

    return board


# check game board full
def isFull(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "":
                return False
    return True


def get_buildable(game_board):
    buildable_coords = []
    is_empty = True
    for row in range(0, len(game_board)):
        for column in range(0, len(game_board)):
            if game_board[row][column] == "":
                continue
            is_empty = False
            item_above, item_below, item_right, item_left = get_items_around(
                game_board, row, column
            )
            if item_above == "" or None:
                buildable_coords.append((row - 1, column))
            if item_below == "" or None:
                buildable_coords.append((row + 1, column))
            if item_left == "" or None:
                buildable_coords.append((row, column - 1))
            if item_right == "" or None:
                buildable_coords.append((row, column + 1))
    if is_empty:
        # Return coordinates for every single position on board
        buildable_coords = [
            (row, col)
            for col in range(len(game_board[row]))
            for row in range(len(game_board))
        ]
    return buildable_coords


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


def get_items_around(game_board, i, y):
    # obtains items around a given coordinate.
    # Returns none for an item if it's out-of-bounds
    # Prevent negative indexing by ensuring it's more than 0
    if (i - 1) >= 0:
        item_above = game_board[i - 1][y]
    else:
        item_above = None
    try:
        item_below = game_board[i + 1][y]
    except IndexError:
        item_below = None
    try:
        item_right = game_board[i][y + 1]
    except IndexError:
        item_right = None
    # Prevent negative indexing by ensuring it's more than 0
    if (y - 1) >= 0:
        item_left = game_board[i][y - 1]
    else:
        item_left = None
    return item_above, item_below, item_right, item_left