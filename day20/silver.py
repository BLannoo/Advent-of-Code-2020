import math
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple, Dict, List, Iterable, Set, Optional

TILE_SIZE = 10


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
    assert tiles[2311].re_orient(Orientation(True)) in flipped_1951.tiles_that_match_right(tiles)
    assert tiles[2729].re_orient(Orientation(True)) in flipped_1951.tiles_that_match_bellow(tiles)

    solution = solve(tiles)
    print(solution)
    solution.save_picture("example_picture.txt")
    assert 20899048083289 == solution.check_sum()


def test_silver():
    tiles = load("input.txt")
    solution = solve(tiles)
    solution.save_picture("input_picture.txt")
    assert 32287787075651 == solution.check_sum()


@dataclass(frozen=True)
class Orientation:
    flip: bool = False
    right_rotations: int = 0

    def __repr__(self):
        return (
                ("F" if self.flip else ".")
                +
                "R" * self.right_rotations
                +
                "." * (3 - self.right_rotations)
        )

    def fliped(self):
        return Orientation(not self.flip, self.right_rotations)

    def rotate_right(self):
        return Orientation(self.flip, self.right_rotations + 1)


ALL_ORIENTATIONS = tuple(
    Orientation(flip, rotation)
    for flip in (True, False)
    for rotation in range(4)
)


@dataclass(frozen=True)
class Tile:
    number: int
    pattern: Tuple[Tuple[str, ...], ...]
    orientation: Orientation
    size: int = TILE_SIZE

    def __repr__(self):
        return f"{self.number}-{self.orientation}"

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
            Orientation(),
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
        return Tile(self.number, self.pattern[::-1], self.orientation.fliped())

    @lru_cache
    def rotate_right(self) -> "Tile":
        return Tile(
            self.number,
            tuple(
                tuple(
                    self.pattern[-x - 1][y]
                    for x in range(self.size)
                )
                for y in range(self.size)
            ),
            self.orientation.rotate_right(),
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

    @lru_cache
    def re_orient(self, orientation: Orientation) -> "Tile":
        re_oriented_tile = self
        if orientation.flip:
            re_oriented_tile = re_oriented_tile.flip_horizontally()
        for _ in range(orientation.right_rotations):
            re_oriented_tile = re_oriented_tile.rotate_right()
        return re_oriented_tile

    def tiles_that_match_right(self, tiles: Dict[int, "Tile"]) -> Set["Tile"]:
        return {
            tile.re_orient(orientation)
            for tile_number, tile in tiles.items()
            for orientation in ALL_ORIENTATIONS
            if self.matches_left_of(tile.re_orient(orientation))
        }

    def tiles_that_match_bellow(self, tiles: Dict[int, "Tile"]) -> Set["Tile"]:
        return {
            tile.re_orient(orientation)
            for tile_number, tile in tiles.items()
            for orientation in ALL_ORIENTATIONS
            if self.matches_above_of(tile.re_orient(orientation))
        }


class Solution:
    tiles: Dict[int, Tile]
    solution: List[List[Optional[Tile]]]

    def __init__(self, tiles: Dict[int, Tile], solution: List[List[Optional[Tile]]]):
        self.tiles = tiles
        self.solution = solution

    def __repr__(self):
        return f"\nSolution: {self.next_slot()=}\n" + "\n".join(
            "\t".join(
                str(cell) if cell else "None"
                for cell in line
            )
            for line in self.solution
        )

    @staticmethod
    def seed_solution(tile: Tile, tiles: Dict[int, Tile]) -> "Solution":
        size = int(math.sqrt(len(tiles)))
        empty_solution: List[List[Optional[Tile]]] = [
            [
                None
                for _ in range(size)
            ]
            for _ in range(size)
        ]
        empty_solution[0][0] = tile
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

        available_tiles = self.available_tiles()

        valid_next_tiles = {
            tile.re_orient(orientation)
            for tile in available_tiles.values()
            for orientation in ALL_ORIENTATIONS
        }

        if x > 0:
            valid_next_tiles = self.solution[y][x - 1].tiles_that_match_right(available_tiles)
        if y > 0:
            valid_next_tiles = self.solution[y - 1][x].tiles_that_match_bellow(available_tiles)
        if x > 0 and y > 0:
            tiles_that_match_right = self.solution[y][x - 1].tiles_that_match_right(available_tiles)
            tiles_that_match_bellow = self.solution[y - 1][x].tiles_that_match_bellow(available_tiles)
            valid_next_tiles = tiles_that_match_right.intersection(tiles_that_match_bellow)

        return [
            self.fill_next_slot_with(tile)
            for tile in valid_next_tiles
        ]

    def fill_next_slot_with(self, tile: Tile) -> "Solution":
        solution_copy = [
            [
                tile if (x, y) == self.next_slot() else cell
                for x, cell in enumerate(line)
            ]
            for y, line in enumerate(self.solution)
        ]
        return Solution(self.tiles, solution_copy)

    def available_tiles(self) -> Dict[int, Tile]:
        return {
            tile.number: tile
            for tile in self.tiles.values()
            if tile.number not in map(lambda tile: tile.number, self.placed_tiles())
        }

    def placed_tiles(self) -> Set[Tile]:
        return {
            cell
            for line in self.solution
            for cell in line
            if cell
        }

    def check_sum(self) -> int:
        return (
                self.solution[0][0].number
                *
                self.solution[0][-1].number
                *
                self.solution[-1][0].number
                *
                self.solution[-1][-1].number
        )

    def save_picture(self, file_name: str):
        picture = ""
        for y_tile, line in enumerate(self.solution):
            for y_pixel in range(1, TILE_SIZE - 1):
                for x_tile, cell in enumerate(line):
                    for x_pixel in range(1, TILE_SIZE - 1):
                        picture += self.solution[x_tile][y_tile].pattern[x_pixel][y_pixel]
                picture += "\n"
        with open(file_name, "w") as file:
            file.write(picture)


def solve(tiles: Dict[int, Tile]) -> Solution:
    candidates = [
        Solution.seed_solution(tile.re_orient(orientation), tiles)
        for tile in tiles.values()
        for orientation in ALL_ORIENTATIONS
    ]
    while not candidates[-1].is_solved():
        candidate = candidates.pop()
        candidates.extend(candidate.fill_next_slot())
    return candidates[-1]


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
