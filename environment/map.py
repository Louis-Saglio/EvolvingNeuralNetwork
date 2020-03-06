from typing import List


class Cell:
    def __init__(self):
        self.stack = []
        self.neighbours: List[Cell] = []
