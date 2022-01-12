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

#load test         
@pytest.mark.parametrize("board, pool, expectedBoard, expectedPool", [([['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},  
                                                       [['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8})])
def test_load_game(fs, board, pool, expectedBoard, expectedPool):
    pickle_out = open('load_test.pickle', "wb")
    pickle.dump([board, pool], pickle_out)
    pickle_out.close()
    eBoard,ePool = load_game('load_test.pickle')
    assert eBoard == expectedBoard
    assert ePool ==  expectedPool

# saving test        
@pytest.mark.parametrize("board, pool, expectedBoard, expectedPool", [([['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},  
                                                         [['', '', '', ''], ['', '', '', '']], {'HSE': 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8})])
def test_save_game(board, pool, expectedBoard, expectedPool,fs):
    save_game (board, pool, 'save_test.pickle')
    pickle_in = open('save_test.pickle', "rb")
    sBoard = pickle.load(pickle_in)
    assert sBoard[0] == expectedBoard
    assert sBoard[1] ==  expectedPool