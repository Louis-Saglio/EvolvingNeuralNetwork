from unittest import TestCase

from map import Cell
from models import Spacial


class TestSpacial(TestCase):
    def test_move(self):
        cell = Cell()
        cell.neighbours = [Cell(), Cell(), Cell(), Cell()]
        spacial = Spacial(cell)
        spacial.move(0)

        self.assertIs(spacial.cell, cell.neighbours[0])
        self.assertNotIn(spacial, cell.stack)
        self.assertIn(spacial, spacial.cell.stack)

    def test_move_to_absent_destination(self):
        cell = Cell()
        cell.neighbours = [Cell(), Cell()]
        spacial = Spacial(cell)
        spacial.move(3)

        self.assertIs(spacial.cell, cell)
        self.assertIn(spacial, cell.stack)
        self.assertIn(spacial, cell.stack)
