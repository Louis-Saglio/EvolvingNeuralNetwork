from __future__ import annotations

from typing import List, Callable

from map import Cell

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

    def move(self, to: int):
        if len(self.cell.neighbours) > to:
            self.cell.stack.remove(self)
            self.cell = self.cell.neighbours[to]
            self.cell.stack.append(self)


class Universe:
    def __init__(self):
        self.individuals: List[Individual] = []

    def run(self):
        while True:
            for individual in self.individuals:
                individual.run()
