from unittest import TestCase

from map import Cell
from models import Individual


class TestIndividual(TestCase):
    def test_move(self):
        cell = Cell()
        cell.neighbours = [Cell(), Cell(), Cell(), Cell()]
        individual = Individual(cell, [])
        individual.move(0)

        self.assertIs(individual.cell, cell.neighbours[0])
        self.assertNotIn(individual, cell.stack)
        self.assertIn(individual, individual.cell.stack)

    def test_move_to_absent_destination(self):
        cell = Cell()
        cell.neighbours = [Cell(), Cell()]
        individual = Individual(cell, [])
        individual.move(3)

        self.assertIs(individual.cell, cell)
        self.assertIn(individual, cell.stack)
        self.assertIn(individual, cell.stack)
