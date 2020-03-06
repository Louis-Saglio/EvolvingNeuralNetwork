from typing import Dict, Tuple

from environment.map import Cell
from genetic_algorithm import Individual


def build_2d_map(width: int, height: int) -> Dict[Tuple[int, int], Cell]:
    cells_by_position = {}
    for w in range(width):
        for h in range(height):
            cells_by_position[(w, h)] = Cell()
    for position, cell in cells_by_position.items():
        for neighbour_position_delta in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbour = cells_by_position.get(
                (
                    position[0] + neighbour_position_delta[0],
                    position[1] + neighbour_position_delta[1],
                )
            )
            if neighbour:
                cell.neighbours.append(neighbour)
    return cells_by_position


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
