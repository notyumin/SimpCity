import pytest
from simpCity import *
import pickle


def test_init_game_creates_game_board_and_pool():
    # Act
    game_board, building_pool = init_game()

    # Assert
    assert game_board == [['', '', '', ''], ['', '', '', ''],
                          ['', '', '', ''], ['', '', '', ''], ]
    assert building_pool == {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8}


@pytest.mark.parametrize("board, pool, expectedBoard, expectedPool", [([['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},  
                                                        [['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8})])
def test_save_and_load_game(board, pool, expectedBoard, expectedPool):
    save_game (board, pool)
    eBoard,ePool = load_game()
    assert eBoard == expectedBoard
    assert ePool ==  expectedPool

#load test         doesnt work need help due to fs 
# @pytest.mark.parametrize("board, pool, expectedBoard, expectedPool", [([['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},  
#                                                         [['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8})])
# def test_load_game(fs):
#     board = [['HSE', '', '', ''], ['', '', '', ''],
#                           ['', '', '', ''], ['', '', '', ''], ]
#     pool = {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8}
#     pickle_out = open(fs.create_file('load_test.pickle'), "wb")
#     pickle.dump([board, pool], pickle_out)
#     eBoard,ePool = load_game()
#     assert eBoard == board
#     assert ePool ==  pool

#saving test        doesnt work need help due to fs
# @pytest.mark.parametrize("board, pool, expectedBoard, expectedPool", [([['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},  
#                                                         [['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8})])
# def test_save_game(board, pool, expectedBoard, expectedPool,fs):
#     filename = fs.create_file('save_test.pickle')
#     save_game (board, pool, filename)
#     pickle_in = open(filename, "rb")
#     sBoard = pickle.load(pickle_in)
#     assert sBoard[0] == expectedBoard
#     assert sBoard[1] ==  expectedPool