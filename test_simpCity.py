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
