import pytest
from simpCity import *
import pickle


def test_init_game_creates_game_board_and_pool():
    # Act
    game_board, building_pool = init_game()

    # Assert
    assert game_board == [
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
    ]
    assert building_pool == {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8}


@pytest.mark.parametrize(
    "pool,  expected_buildings",
    [
        (
            {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},
            ["HSE", "FAC", "SHP", "HWY", "BCH"],
        ),
        ({"HSE": 0, "FAC": 0, "SHP": 0, "HWY": 0, "BCH": 8}, ["BCH"]),
        ({"HSE": 0, "FAC": 0, "SHP": 0, "HWY": 0, "BCH": 1}, ["BCH", None]),
        ({"HSE": 0, "FAC": 0, "SHP": 0, "HWY": 0, "BCH": 0}, [None]),
    ],
)
def test_randomise_buildings_returns_valid_building(pool, expected_buildings):
    # Act
    buildings = randomise_building(pool)

    # Assert
    assert buildings[0] in expected_buildings
    assert buildings[1] in expected_buildings


# load test
@pytest.mark.parametrize(
    "board, pool, expectedBoard, expectedPool",
    [
        (
            [["", "", "", ""], ["", "", "", ""]],
            {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},
            [["", "", "", ""], ["", "", "", ""]],
            {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},
        )
    ],
)
def test_load_game(fs, board, pool, expectedBoard, expectedPool):
    pickle_out = open("load_test.pickle", "wb")
    pickle.dump([board, pool], pickle_out)
    pickle_out.close()
    eBoard, ePool = load_game("load_test.pickle")
    assert eBoard == expectedBoard
    assert ePool == expectedPool


# saving test
@pytest.mark.parametrize(
    "board, pool, expectedBoard, expectedPool",
    [
        (
            [["", "", "", ""], ["", "", "", ""]],
            {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},
            [["", "", "", ""], ["", "", "", ""]],
            {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},
        )
    ],
)
def test_save_game(board, pool, expectedBoard, expectedPool, fs):
    save_game(board, pool, "save_test.pickle")
    pickle_in = open("save_test.pickle", "rb")
    sBoard = pickle.load(pickle_in)
    assert sBoard[0] == expectedBoard
    assert sBoard[1] == expectedPool


@pytest.mark.parametrize(
    "board,column,row,building,expected_board",
    [
        (
            [
                ["", "HWY", "", ""],
                ["", "SHP", "HSE", "BCH"],
                ["", "HSE", "HSE", "BCH"],
                ["", "", "", ""],
            ],
            "A",
            "1",
            "HWY",
            [
                ["HWY", "HWY", "", ""],
                ["", "SHP", "HSE", "BCH"],
                ["", "HSE", "HSE", "BCH"],
                ["", "", "", ""],
            ],
        ),
        (
            [
                ["", "HWY", "", ""],
                ["", "SHP", "HSE", "BCH"],
                ["", "HSE", "HSE", "BCH"],
                ["", "", "", ""],
            ],
            "A",
            "3",
            "BCH",
            [
                ["", "HWY", "", ""],
                ["", "SHP", "HSE", "BCH"],
                ["BCH", "HSE", "HSE", "BCH"],
                ["", "", "", ""],
            ],
        ),
    ],
)
def test_build_places_building_in_board(board, column, row, building, expected_board):
    new_board = build(board, column, row, building)

    assert new_board == expected_board


@pytest.mark.parametrize(
    "board,column,row,building",
    [
        (
            [
                ["", "HWY", "", ""],
                ["", "SHP", "HSE", "BCH"],
                ["", "HSE", "HSE", "BCH"],
                ["", "", "", ""],
            ],
            "B",
            "2",
            "HWY",
        ),
        (
            [
                ["", "HWY", "", ""],
                ["", "SHP", "HSE", "BCH"],
                ["", "HSE", "HSE", "BCH"],
                ["", "", "", ""],
            ],
            "E",
            "3",
            "BCH",
        ),
    ],
)
def test_build_throws_error_for_invalid_placement(board, column, row, building):
    with pytest.raises(Exception) as e_info:
        new_board = build(board, column, row, building)


@pytest.mark.parametrize("board, expected_score", [
    (
        [
            ["HWY", "HWY", "HWY", "FAC"],
            ["BCH", "HSE", "HSE", "SHP"],
            ["BCH", "SHP", "HSE", "FAC"],
            ["HWY", "FAC", "HWY", "HWY"]
        ],
        42
    ),
    (
        [
            ["", "HWY", "", ""],
            ["", "SHP", "HSE", "BCH"],
            ["", "HSE", "HSE", "BCH"],
            ["", "", "", ""]
        ],
        19
    ),
    (
        [
            ["", "HSE", "FAC", "BCH"],
            ["", "FAC", "BCH", ""],
            ["", "SHP", "", "BCH"],
            ["HWY", "", "", ""]
        ],
        14
    ),
    (
        [
            ["PRK", "PRK", "", "", "MON"],
            ["PRK", "PRK", "", "", ""],
            ["", "", "", "", ""],
            ["", "MON", "", "MON", ""],
            ["MON", "", "", "", "MON"]
        ],
        36
    ),
    (
        [
            ["PRK", "PRK", "", "", "PRK"],
            ["PRK", "PRK", "", "", "PRK"],
            ["", "", "PRK", "", "PRK"],
            ["", "MON", "", "MON", ""],
            ["MON", "", "", "", "MON"]
        ],
        31
    ),
    (
        [
            ["PRK", "PRK", "PRK", "", ""],
            ["PRK", "PRK", "", "", ""],
            ["PRK", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""]
        ],
        23
    ),
])
def test_calculate_score_returns_valid_score(board, expected_score):
    # Act
    calculated_score = calculate_score(board)

    # Assert
    assert calculated_score == expected_score


@pytest.mark.parametrize("board, expected_park_coords", [
    (
        [
            ["PRK", "PRK", "PRK", "PRK"],
            ["PRK", "", "", "PRK"],
            ["PRK", "", "", "PRK"],
            ["PRK", "PRK", "PRK", "PRK"]
        ],
        [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2),
         (3, 3), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1)]
    ),
    (
        [
            ["PRK", "PRK", "", ""],
            ["PRK", "PRK", "", ""],
            ["", "", "", ""],
            ["", "", "", ""]
        ],
        [(0, 0), (1, 0), (1, 1), (0, 1)]
    ),
    (
        [
            ["PRK", "PRK", "PRK", "PRK", "PRK"],
            ["PRK",    "", "PRK",    "", "PRK"],
            ["PRK",    "", "PRK",    "", "PRK"],
            ["PRK", "PRK", "PRK", "PRK", "PRK"]
        ],
        [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2),
         (3, 3), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (1, 2), (2, 2), (0, 1)]
    ),
    (
        [
            ["PRK", "PRK", "PRK", "PRK"],
            ["", "PRK",   "",     ""],
            ["", "PRK",   "",     ""],
            ["PRK", "PRK", "PRK", "PRK"]
        ],
        [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
         (2, 1), (3, 0), (3, 1), (3, 2), (3, 3)]
    ),
])
def test_crawl_parks_obtains_coords_list_of_horizontally_and_vertically_connected_parks(board, expected_park_coords):
    # Act
    park_coordinates = crawl_parks(board, 0, 0, [])

    # Assert using sets because order of list does not matter
    assert set(park_coordinates) == set(expected_park_coords)
