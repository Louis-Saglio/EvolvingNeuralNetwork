from __future__ import annotations

from random import choice
from typing import List, Callable

from map import Cell
from twodmap import build_2d_map, move_left, move_right, move_down, move_up

Action = Callable[["Individual"], None]


class Individual:
    def __init__(self, cell: Cell, possible_actions: List[Action]):
        self.cell: Cell = cell
        cell.stack.append(self)
        self.possible_actions = possible_actions

    def choose_action(self) -> Action:
        raise NotImplementedError

    def run(self):
        self.choose_action()(self)


class Universe:
    def __init__(self):
        self.individuals: List[Individual] = []

    def run(self):
        while True:
            for individual in self.individuals:
                individual.run()


def main():
    class RandomIndividual(Individual):
        def choose_action(self) -> Action:
            return choice(self.possible_actions)

    universe = Universe()
    cells = list(build_2d_map(10, 10).values())
    universe.individuals = [
        RandomIndividual(choice(cells), [move_left, move_right, move_down, move_up])
        for _ in range(10)
    ]
    universe.run()


if __name__ == "__main__":
    main()
