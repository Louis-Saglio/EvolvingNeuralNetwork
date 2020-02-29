from typing import List, Dict, Tuple


class Cell:
    def __init__(self):
        self.stack = []
        self.neighbours: List[Cell] = []


def build_2d_map(width: int, height: int) -> Dict[Tuple[int, int], Cell]:
    cells_by_position = {}
    for w in range(width):
        for h in range(height):
            cells_by_position[(w, h)] = Cell()
    for position, cell in cells_by_position.items():
        for neighbour_position_delta in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbour = cells_by_position.get(
                (position[0] + neighbour_position_delta[0], position[1] + neighbour_position_delta[1],)
            )
            if neighbour:
                cell.neighbours.append(neighbour)
    return cells_by_position
