from typing import Dict, Tuple

from environment.map import Cell
from models import Individual


class Direction:
    directions = {}

    def __init__(self, name: str, vector: Tuple[int, int]):
        self.name = name
        self.vector = vector
        type(self).directions[name] = self


DIRECTIONS = LEFT, RIGHT, UP, DOWN = (
    Direction("left", (-1, 0)),
    Direction("right", (1, 0)),
    Direction("up", (0, -1)),
    Direction("down", (0, 1)),
)


class Move:
    def __init__(self, direction: Direction):
        self.direction = direction

    def __call__(self, individual: Individual):
        individual.move(DIRECTIONS.index(self.direction))


def build_2d_map(width: int, height: int) -> Dict[Tuple[int, int], Cell]:
    cells_by_position = {}
    for w in range(width):
        for h in range(height):
            cells_by_position[(w, h)] = Cell()
    for position, cell in cells_by_position.items():
        for neighbour_position_delta in DIRECTIONS:
            neighbour = cells_by_position.get(
                (
                    position[0] + neighbour_position_delta.vector[0],
                    position[1] + neighbour_position_delta.vector[1],
                )
            )
            if neighbour:
                cell.neighbours.append(neighbour)
    return cells_by_position
