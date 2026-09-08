from typing import List, Tuple

HEX_CELL_TO_ASCII = {
                0 : "0",
                1 : "1",
                2 : "2",
                3 : "3",
                4 : "4",
                5 : "5",
                6 : "6",
                7 : "7",
                8 : "8",
                9 : "9",
                10 : "a",
                11 : "b",
                12 : "c",
                13 : "d",
                14 : "e",
                15 : "f",
            }

ASCII_TO_HEX_CELL = {v: k for k, v in HEX_CELL_TO_ASCII.items()}

class Cell():
    def __init__(self, hex_cell):
        self.west: bool = hex_cell // 8 == 1
        hex_cell -= 8 if self.west else 0
        self.south: bool = hex_cell // 4 == 1
        hex_cell -= 4 if self.south else 0
        self.east: bool = hex_cell // 2 == 1
        hex_cell -= 2 if self.east else 0
        self.north: bool = hex_cell // 1 == 1

    @property
    def hex_cell(self) -> int:
        return ((self.west * 8) + (self.south * 4) + (self.east * 2) + (self.north * 1))

    def __str__(self):
        return (HEX_CELL_TO_ASCII[self.hex_cell])

    @property
    def is_closed(self):
        return (self.hex_cell == 15)

class Maze():
    def __init__(self, config):
