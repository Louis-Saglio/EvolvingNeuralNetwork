from __future__ import annotations

from typing import List

from environment.utils import DelayedUpdateMixin


class Action:
    def __init__(self, energy: float):
        self.energy = energy

    def __call__(self, individual: Individual, universe: Universe):
        raise NotImplementedError


# Comment gérer le fait qu'un individu peut faire telle ou telle action
# Une action doit elle être un singleton


class EnergyStorage:
    biomass = 1000

    def __init__(self, energy_amount: float):
        self._biomass = 0
        self.add_energy(energy_amount)

    def add_energy(self, energy_amount: float):
        self._biomass += energy_amount
        self.__class__.biomass -= energy_amount


class Individual(DelayedUpdateMixin):
    def __init__(self, energy: float, box: Box, possible_actions: List[Action]):
        super().__init__()
        self._energy = EnergyStorage(energy)
        self.box = box
        self.possible_actions = possible_actions

    def __setattr__(self, name, value):
        if name == "energy":
            self._energy.add_energy(value)
        else:
            super(Individual, self).__setattr__(name, value)

    def choose_action(self) -> Action:
        raise NotImplementedError

    def run(self) -> Action:
        next_action = self.choose_action()
        self.delay_update("energy", next_action.energy * self.box.get_cost_of_action(next_action))
        return next_action


class Box:
    def __init__(self):
        self.neighbours: List[Box] = []

    def get_cost_of_action(self, action: Action) -> float:
        raise NotImplementedError


class Universe:
    def __init__(self, energy: float, population: List[Individual]):
        self.energy = energy
        self.population = population

    def run(self):
        for individual in self.population:
            individual.run()(individual, self)
