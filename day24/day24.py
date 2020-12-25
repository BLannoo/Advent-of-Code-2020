from collections import Counter
from dataclasses import dataclass
from typing import Tuple, Dict, Set, Callable

import regex as regex


def test_silver_example():
    assert 10 == len(setup_floor("example.txt"))


def test_silver():
    assert 394 == len(setup_floor("input.txt"))


def test_gold_example():
    floor = setup_floor("example.txt")
    assert 15 == len(floor := tick(floor, 1))
    assert 12 == len(floor := tick(floor, 1))
    assert 25 == len(floor := tick(floor, 1))
    assert 14 == len(floor := tick(floor, 1))
    assert 23 == len(floor := tick(floor, 1))
    assert 28 == len(floor := tick(floor, 1))
    assert 41 == len(floor := tick(floor, 1))
    assert 37 == len(floor := tick(floor, 1))
    assert 49 == len(floor := tick(floor, 1))
    assert 37 == len(floor := tick(floor, 1))

    assert 132 == len(floor := tick(floor, 10))
    assert 259 == len(floor := tick(floor, 10))
    assert 406 == len(floor := tick(floor, 10))
    assert 566 == len(floor := tick(floor, 10))
    assert 788 == len(floor := tick(floor, 10))
    assert 1106 == len(floor := tick(floor, 10))
    assert 1373 == len(floor := tick(floor, 10))
    assert 1844 == len(floor := tick(floor, 10))
    assert 2208 == len(floor := tick(floor, 10))


def test_gold():
    assert 4036 == len(tick(setup_floor("input.txt"), 100))


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int

    def __add__(self, other: "Coordinates") -> "Coordinates":
        return Coordinates(self.x + other.x, self.y + other.y)

    @staticmethod
    def from_path(path: str) -> "Coordinates":
        return sum(
            (
                DIR_DELTAS[direction]
                for direction in regex.match(r"^(e|se|sw|w|nw|ne)*$", path).captures(1)
            ),
            start=Coordinates(0, 0)
        )

    def neighbours(self) -> Set["Coordinates"]:
        return {
            self + direction
            for direction in DIR_DELTAS.values()
        }


DIR_DELTAS = {
    "e": Coordinates(1, 0),
    "se": Coordinates(1, -1),
    "sw": Coordinates(0, -1),
    "w": Coordinates(-1, 0),
    "nw": Coordinates(-1, 1),
    "ne": Coordinates(0, 1),
}


def tick(black_tiles: Set[Coordinates], iterations: int = 1) -> Set[Coordinates]:
    for _ in range(iterations):
        black_tiles = tick_once(black_tiles)
    return black_tiles


def tick_once(yesterdays_black_tiles: Set[Coordinates]) -> Set[Coordinates]:
    tomorrows_black_tiles = apply_rules(yesterdays_black_tiles)
    return {
        cell
        for cell in potential_black_tiles(yesterdays_black_tiles)
        if tomorrows_black_tiles(cell)
    }


def apply_rules(yesterdays_black_tiles: Set[Coordinates]) -> Callable[[Coordinates], bool]:
    def tomorrows_black_tiles(tile: Coordinates) -> bool:
        neighbouring_black_tiles = len(tile.neighbours().intersection(yesterdays_black_tiles))
        return (
                (neighbouring_black_tiles == 2)
                or
                (tile in yesterdays_black_tiles and neighbouring_black_tiles == 1)
        )

    return tomorrows_black_tiles


def potential_black_tiles(old_floor: Set[Coordinates]) -> Set[Coordinates]:
    return {
        old_tile_neighbour
        for old_tile in old_floor
        for old_tile_neighbour in old_tile.neighbours()
    }.union(old_floor)


def setup_floor(file_name: str) -> Set[Coordinates]:
    with open(file_name) as file:
        counts: Dict[Coordinates, int] = Counter(
            Coordinates.from_path(path)
            for path in file.read().split("\n")
        )
        return {
            tile
            for tile, count in counts.items()
            if count % 2 == 1
        }
