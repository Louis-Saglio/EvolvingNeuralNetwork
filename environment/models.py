from __future__ import annotations

from typing import List, Union

from map import Cell


EnergyAmount = Union[int, float]


class Action:
    def __init__(self, required_energy: EnergyAmount):
        self.required_energy = required_energy

    def __call__(self, actor: Actor):
        raise NotImplementedError


class Spacial:
    def __init__(self, cell: Cell):
        self.cell = cell
        self.cell.stack.append(self)

    def move(self, to: int):
        if len(self.cell.neighbours) > to:
            self.cell.stack.remove(self)
            self.cell = self.cell.neighbours[to]
            self.cell.stack.append(self)


class Actor:
    def __init__(self, possible_actions: List[Action], initial_energy_level: EnergyAmount):
        self.possible_actions = possible_actions
        self.energy_level = initial_energy_level

    def choose_action(self) -> Action:
        raise NotImplementedError

    def act(self) -> EnergyAmount:
        if self.energy_level > 0:
            action = self.choose_action()
            if self.energy_level >= action.required_energy:
                self.energy_level -= action.required_energy
                action(self)
            spent_energy = action.required_energy
        else:
            spent_energy = 0
        return spent_energy


class Universe:
    def __init__(self):
        self.actors: List[Actor] = []

    def run(self):
        while True:
            for actor in self.actors:
                actor.act()
