from unittest import TestCase

from src.common import get_surrounding_tile_values, convert_to_frames

layout = [[33, 0, 3],
          [1, 2, 3],
          [3, 3, 39]]


class Test(TestCase):
    def test_get_surrounding_tile_values(self):
        self.assertEqual({0, 1, 2, 3}, get_surrounding_tile_values((1, 1), layout))
        self.assertEqual({0, 3}, get_surrounding_tile_values((0, 2), layout))
        self.assertEqual({1, 3}, get_surrounding_tile_values((2, 0), layout))
        self.assertEqual({0, 1, 33}, get_surrounding_tile_values((0, 0), layout))
        self.assertEqual({3, 39}, get_surrounding_tile_values((2, 2), layout))
        self.assertEqual({39}, get_surrounding_tile_values((2, 3), layout))
        self.assertEqual({3, 39}, get_surrounding_tile_values((-1, 2), layout))
        self.assertEqual({3, 39}, get_surrounding_tile_values((2, -1), layout))
        self.assertEqual({39}, get_surrounding_tile_values((3, 2), layout))

    def test_convert_to_frames(self):
        self.assertEqual(0.6, convert_to_frames(10))
