import math
import re
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations
from pprint import pprint
from typing import Tuple, Dict, List, Iterable, Set, Optional


def test_silver_example():
    tiles = load("example.txt")

    assert tuple(".#####..#.") == tiles[2311].left_border()
    assert tuple("...#.##..#") == tiles[2311].right_border()
    assert tuple("..###..###") == tiles[2311].bottom_border()
    assert tuple("..##.#..#.") == tiles[2311].top_border()

    assert tuple(".#..#####.") == tiles[2311].flip_horizontally().left_border()
    assert tuple("#..##.#...") == tiles[2311].flip_horizontally().right_border()
    assert tuple("..##.#..#.") == tiles[2311].flip_horizontally().bottom_border()
    assert tuple("..###..###") == tiles[2311].flip_horizontally().top_border()

    assert tuple("..###..###") == tiles[2311].rotate_right().left_border()
    assert tuple("..##.#..#.") == tiles[2311].rotate_right().right_border()
    assert tuple("#..##.#...") == tiles[2311].rotate_right().bottom_border()
    assert tuple(".#..#####.") == tiles[2311].rotate_right().top_border()

    assert tiles[1951].flip_horizontally().matches_left_of(tiles[2311].flip_horizontally())
    assert tiles[1951].flip_horizontally().matches_above_of(tiles[2729].flip_horizontally())

    assert (Orientation(True), Orientation(True)) in tiles[1951].find_orientations_for_match_left_of(tiles[2311])
    assert (Orientation(True), Orientation(True)) in tiles[1951].find_orientations_for_match_above_of(tiles[2729])

    flipped_1951 = tiles[1951].re_orient(Orientation(True))
    assert OrientedTile(tiles[2311], Orientation(True)) in flipped_1951.tiles_that_match_right(tiles)
    assert OrientedTile(tiles[2729], Orientation(True)) in flipped_1951.tiles_that_match_bellow(tiles)

    # assert is_solution((
    #     ((1951, Orientation(True)), (2311, Orientation(True)), (3079, Orientation()),),
    #     ((2729, Orientation(True)), (1427, Orientation(True)), (2473, Orientation(True, 3)),),
    #     ((2971, Orientation(True)), (1489, Orientation(True)), (1171, Orientation(True, 2)),),
    # ))

    assert 20899048083289 == solve(tiles)


@dataclass(frozen=True)
class Orientation:
    flip: bool = False
    right_rotations: int = 0


ALL_ORIENTATIONS = tuple(
    Orientation(flip, rotation)
    for flip in (True, False)
    for rotation in range(4)
)


@dataclass(frozen=True)
class Tile:
    number: int
    pattern: Tuple[Tuple[str, ...], ...]
    size: int = 10

    @classmethod
    def create(cls, description: str) -> "Tile":
        match = re.match(r"Tile (\d+):((\n.*)*)$", description)
        if not match:
            print(description)
        return Tile(
            int(match.group(1)),
            tuple(
                tuple(line)
                for line in match.group(2).strip().split("\n")
            ),
        )

    def right_border(self) -> Tuple[str]:
        return tuple(line[-1] for line in self.pattern)

    def left_border(self) -> Tuple[str]:
        return tuple(line[0] for line in self.pattern)

    def bottom_border(self) -> Tuple[str]:
        return tuple(self.pattern[-1])

    def top_border(self) -> Tuple[str]:
        return tuple(self.pattern[0])

    def flip_horizontally(self) -> "Tile":
        return Tile(self.number, self.pattern[::-1])

    def rotate_right(self) -> "Tile":
        return Tile(
            self.number,
            tuple(
                tuple(
                    self.pattern[-x - 1][y]
                    for x in range(self.size)
                )
                for y in range(self.size)
            )
        )

    def matches_left_of(self, right_tile: "Tile") -> bool:
        return self.right_border() == right_tile.left_border()

    def matches_above_of(self, bottom_tile: "Tile") -> bool:
        return self.bottom_border() == bottom_tile.top_border()

    def find_orientations_for_match_left_of(
            self,
            right_tile: "Tile",
            left_orientations: Iterable[Orientation] = ALL_ORIENTATIONS,
            right_orientations: Iterable[Orientation] = ALL_ORIENTATIONS,
    ) -> List[Tuple[Orientation, Orientation]]:
        return [
            (orientation_left_tile, orientation_right_tile)
            for orientation_left_tile in left_orientations
            for orientation_right_tile in right_orientations
            if self.re_orient(orientation_left_tile).matches_left_of(right_tile.re_orient(orientation_right_tile))
        ]

    def find_orientations_for_match_above_of(
            self,
            bottom_tile: "Tile",
            top_orientations: Iterable[Orientation] = ALL_ORIENTATIONS,
            bottom_orientations: Iterable[Orientation] = ALL_ORIENTATIONS,
    ) -> List[Tuple[Orientation, Orientation]]:
        return [
            (orientation_top_tile, orientation_bottom_tile)
            for orientation_top_tile in top_orientations
            for orientation_bottom_tile in bottom_orientations
            if self.re_orient(orientation_top_tile).matches_above_of(bottom_tile.re_orient(orientation_bottom_tile))
        ]

    def re_orient(self, orientation: Orientation) -> "Tile":
        re_oriented_tile = self
        if orientation.flip:
            re_oriented_tile = re_oriented_tile.flip_horizontally()
        for _ in range(orientation.right_rotations):
            re_oriented_tile = re_oriented_tile.rotate_right()
        return re_oriented_tile

    def tiles_that_match_right(self, tiles: Dict[int, "Tile"]) -> Set["OrientedTile"]:
        return {
            OrientedTile(tile, orientation)
            for tile_number, tile in tiles.items()
            for orientation in ALL_ORIENTATIONS
            if self.matches_left_of(tile.re_orient(orientation))
        }

    def tiles_that_match_bellow(self, tiles: Dict[int, "Tile"]) -> Set["OrientedTile"]:
        return {
            OrientedTile(tile, orientation)
            for tile_number, tile in tiles.items()
            for orientation in ALL_ORIENTATIONS
            if self.matches_above_of(tile.re_orient(orientation))
        }


@dataclass(frozen=True)
class OrientedTile:
    tile: Tile
    orientation: Orientation


class Solution:
    tiles: Dict[int, Tile]
    solution: List[List[Optional[OrientedTile]]]

    def __init__(self, tiles: Dict[int, Tile], solution: List[List[Optional[OrientedTile]]]):
        self.tiles = tiles
        self.solution = solution

    def __repr__(self):
        return f"\nSolution: {self.next_slot()=}\n" + "\n".join(
            "\t".join(
                str(cell.tile.number) if cell else "None"
                for cell in line
            )
            for line in self.solution
        )

    @staticmethod
    def seed_solution(oriented_tile: OrientedTile, tiles: Dict[int, Tile]) -> "Solution":
        size = int(math.sqrt(len(tiles)))
        empty_solution: List[List[Optional[OrientedTile]]] = [
            [
                None
                for _ in range(size)
            ]
            for _ in range(size)
        ]
        empty_solution[0][0] = oriented_tile
        return Solution(tiles, empty_solution)

    def is_solved(self):
        return self.next_slot() is None

    def next_slot(self):
        for y, line in enumerate(self.solution):
            for x, cell in enumerate(line):
                if cell is None:
                    return x, y

    def fill_next_slot(self) -> List["Solution"]:
        x, y = self.next_slot()
        if x > 0:
            self.solution[x][y]

        valid_next_oriented_tiles = {
            OrientedTile(self.tiles[1951], Orientation())
        }
        return [
            self.fill_next_slot_with(oriented_tile)
            for oriented_tile in valid_next_oriented_tiles
        ]

    def fill_next_slot_with(self, oriented_tile: OrientedTile) -> "Solution":
        solution_copy = [
            [
                oriented_tile if (x, y) == self.next_slot() else cell
                for x, cell in enumerate(line)
            ]
            for y, line in enumerate(self.solution)
        ]
        return Solution(self.tiles, solution_copy)


def solve(tiles: Dict[int, Tile]) -> int:
    candidates = [
        Solution.seed_solution(OrientedTile(tile, orientation), tiles)
        for tile in tiles.values()
        for orientation in ALL_ORIENTATIONS

    ]
    while not candidates[-1].is_solved():
        candidate = candidates.pop()
        print(candidate)
        candidates.extend(candidate.fill_next_slot())
    return len(candidates)


def load(file_name: str) -> Dict[int, Tile]:
    with open(file_name) as file:
        tiles = tuple(
            Tile.create(description)
            for description in file.read().split("\n\n")
        )
        return {
            tile.number: tile
            for tile in tiles
        }
