from random import choice

from models import Action, Universe, Actor, Spacial
from twodmap import build_2d_map, Move, LEFT, RIGHT, UP, DOWN
from utils import MultipleParentsInheritor


def main():
    class RandomIndividual(MultipleParentsInheritor, Actor, Spacial):
        def choose_action(self) -> Action:
            return choice(self.possible_actions)

    universe = Universe()
    cells = list(build_2d_map(10, 10).values())
    universe.actors = [
        RandomIndividual(
            {
                Spacial: {"cell": choice(cells)},
                Actor: {
                    "possible_actions": [Move(LEFT), Move(RIGHT), Move(DOWN), Move(UP)],
                    "initial_energy_level": 100,
                },
            },
        )
        for _ in range(10)
    ]
    universe.run()


if __name__ == "__main__":
    main()
