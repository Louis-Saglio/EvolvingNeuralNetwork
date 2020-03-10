from unittest import TestCase

from map import Cell
from models import Spacial, Actor, Action


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


class TestActor(TestCase):
    def test_choose_action(self):
        with self.assertRaises(NotImplementedError):
            Actor([], 0).choose_action()

    def test_act(self):
        class TestableActor(Actor):
            def choose_action(self):
                return self.possible_actions[0]

        class DoNothing(Action):
            def __call__(self, actor):
                pass

        my_actor = TestableActor([DoNothing(3)], 5)
        my_actor.act()

        self.assertEqual(my_actor.energy_level, 2)
