from random import choice

from models import Individual, Action, Universe
from twodmap import build_2d_map, Move, LEFT, RIGHT, UP, DOWN


def main():
    class RandomIndividual(Individual):
        def choose_action(self) -> Action:
            return choice(self.possible_actions)

    universe = Universe()
    cells = list(build_2d_map(10, 10).values())
    universe.individuals = [
        RandomIndividual(choice(cells), [Move(LEFT), Move(RIGHT), Move(DOWN), Move(UP)], 100)
        for _ in range(10)
    ]
    universe.run()


if __name__ == "__main__":
    main()
