from __future__ import annotations

from random import choice
from typing import List, Callable

from environment.map import Cell, build_2d_map

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


def move(individual: Individual, to: int):
    if len(individual.cell.neighbours) < to:
        individual.cell.stack.remove(individual)
        individual.cell = individual.cell.neighbours[to]
        individual.cell.stack.append(individual)


def move_left(individual: Individual):
    move(individual, 0)


def move_right(individual: Individual):
    move(individual, 1)


def move_down(individual: Individual):
    move(individual, 2)


def move_up(individual: Individual):
    move(individual, 3)


def main():
    class RandomIndividual(Individual):
        def choose_action(self) -> Action:
            return choice(self.possible_actions)

    cells = list(build_2d_map(10, 10).values())
    actions = [move_left, move_right, move_down, move_up]
    universe = Universe()
    universe.individuals = [RandomIndividual(choice(cells), actions) for _ in range(10)]
    universe.run()


if __name__ == "__main__":
    main()
