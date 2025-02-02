import os
from unittest import TestCase
from unittest.mock import patch

from src.common import Direction
from src.game import Game
from src.maps import MapWithoutNPCs
from src.movement import bump_and_reset

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

layout = [[33, 0, 3],
          [1, 2, 3],
          [3, 3, 39]]


class MockMap(MapWithoutNPCs):
    __test__ = False

    def __init__(self):
        super().__init__(layout)

    def hero_underlying_tile(self):
        return 'BRICK'

    def hero_initial_direction(self):
        return Direction.DOWN.value


class Test(TestCase):

    def setUp(self) -> None:
        with patch('src.game.SCALED'):
            self.game = Game()
        self.game.current_map = MockMap()

    def test_bump_and_reset(self):
        self.assertEqual('BRICK', self.game.player.next_tile_id)
        self.assertEqual('RIGHT_FACE_GUARD', self.game.player.next_next_tile_id)
        bump_and_reset(self.game.player, 'TREES', 'GRASS')
        self.assertEqual('TREES', self.game.player.next_tile_id)
        self.assertEqual('GRASS', self.game.player.next_next_tile_id)
