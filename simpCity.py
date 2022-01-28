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
