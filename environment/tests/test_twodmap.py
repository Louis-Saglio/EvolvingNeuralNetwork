from unittest import TestCase

from twodmap import build_2d_map


class Test(TestCase):
    def test_build_2d_map_position_range(self):
        two_d_map = build_2d_map(5, 3)
        self.assertIn((0, 0), two_d_map)
        self.assertIn((4, 2), two_d_map)
        self.assertNotIn((5, 3), two_d_map)
        self.assertIn((1, 1), two_d_map)

    def test_build_2d_map_neighbours(self):
        two_d_map = build_2d_map(3, 3)
        self.assertIs(two_d_map[(1, 1)].neighbours[0], two_d_map[(0, 1)])
        self.assertIs(two_d_map[(1, 1)].neighbours[1], two_d_map[(2, 1)])
        self.assertIs(two_d_map[(1, 1)].neighbours[2], two_d_map[(1, 0)])
        self.assertIs(two_d_map[(1, 1)].neighbours[3], two_d_map[(1, 2)])
