import pytest
from simpCity import *
import pickle


@pytest.mark.parametrize("pool,  expected_buildings", [
    ({"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},
     ["HSE", "FAC", "SHP", "HWY", "BCH"]),
    ({"HSE": 0, "FAC": 0, "SHP": 0, "HWY": 0, "BCH": 8},
     ["BCH"]),
    ({"HSE": 0, "FAC": 0, "SHP": 0, "HWY": 0, "BCH": 1},
     ["BCH", None]),
    ({"HSE": 0, "FAC": 0, "SHP": 0, "HWY": 0, "BCH": 0},
     [None])
])
def test_randomise_buildings_returns_valid_building(pool, expected_buildings):
    # Act
    buildings = randomise_building(pool)

    # Assert
    assert buildings[0] in expected_buildings
    assert buildings[1] in expected_buildings

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
    
# building chosen city size
@pytest.mark.parametrize("size, expectedBoard",[(5, [['', '', '', '', ''], ['', '', '', '', ''],
                          ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']] )])
def test_build_grid(size, expectedBoard):
    board = build_grid(size)
    assert board == expectedBoard

# building chosen building pool
@pytest.mark.parametrize("buildings, size, expectedPool",[(['HSE', 'FAC', 'SHP', 'HWY', 'BCH'], 5, {"HSE": 12, "FAC": 12, "SHP": 12, "HWY": 12, "BCH": 12} )])
def test_build_pool(buildings, size, expectedPool):
    pool = build_pool(buildings, size)
    assert pool == expectedPool

# finalize user's option (size not inputted but building was, building not inputted but size was, both building and size inputted)
@pytest.mark.parametrize("buildings, size, expectedPool, expectedBoard",[(['HSE', 'FAC', 'SHP', 'HWY', 'BCH'], None, {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8}, [['', '', '', ''], ['', '', '', ''],
                          ['', '', '', ''], ['', '', '', ''] ] ), (None, 5, {"HSE": 12, "FAC": 12, "SHP": 12, "HWY": 12, "BCH": 12}, [['', '', '', '', ''], ['', '', '', '', ''],
                          ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']] ), (['PRK', 'FAC', 'SHP', 'HWY', 'MON'], 6, {"PRK": 18, "FAC": 18, "SHP": 18, "HWY": 18, "MON": 18}, [['', '', '', '', '', ''], ['', '', '', '', '', ''],
                          ['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', '']])])
def test_set_game( buildings, size, expectedBoard, expectedPool):
    board, pool = set_game(size, buildings)
    assert pool == expectedPool
    assert board == expectedBoard
