import pytest
from simpCity import init_game, randomise_building


def test_init_game_creates_game_board_and_pool():
    # Act
    game_board, building_pool = init_game()

    # Assert
    assert game_board == [['', '', '', ''], ['', '', '', ''],
                          ['', '', '', ''], ['', '', '', ''], ]
    assert building_pool == {"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8}


@pytest.mark.parametrize("pool,  expected_buildings", [
    ({"HSE": 8, "FAC": 8, "SHP": 8, "HWY": 8, "BCH": 8},
     ["HSE", "FAC", "SHP", "HWY", "BCH"]),
    ({"HSE": 0, "FAC": 0, "SHP": 0,
      "HWY": 0, "BCH": 8}, ["BCH"])
])
def test_randomise_buildings_returns_valid_building(pool, expected_buildings):
    # Act
    building = randomise_building(pool)

    # Assert
    assert building in expected_buildings
