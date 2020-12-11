from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple, Callable, List


def test_silver_example():
    grid = Grid.from_file("example_step0.txt", neighbours_silver)
    grid = grid.tick()
    assert grid == Grid.from_file("example_step1.txt", neighbours_silver)
    grid = grid.tick(4)
    assert grid == Grid.from_file("example_step5_silver.txt", neighbours_silver)
    assert grid == grid.tick()
    assert 37 == grid.count("#")


def test_silver():
    grid = Grid.from_file("input.txt", neighbours_silver)
    next_grid = grid.tick()
    while next_grid != grid:
        grid = next_grid
        next_grid = grid.tick()
    assert 2489 == grid.count("#")


def test_gold_example():
    grid = Grid.from_file("example_step0.txt", neighbours_gold, seaters_tolerance=5)
    grid = grid.tick()
    assert grid == Grid.from_file("example_step1.txt", neighbours_gold, seaters_tolerance=5)
    grid = grid.tick(5)
    assert grid == Grid.from_file("example_step6_gold.txt", neighbours_gold, seaters_tolerance=5)
    assert grid == grid.tick()
    assert 26 == grid.count("#")


def test_gold():
    grid = Grid.from_file("input.txt", neighbours_gold, seaters_tolerance=5)
    next_grid = grid.tick()
    while next_grid != grid:
        grid = next_grid
        next_grid = grid.tick()
    assert 2180 == grid.count("#")


DIRECTIONS = (
    (i, j)
    for i in (-1, 0, 1)
    for j in (-1, 0, 1)
    if not (i == 0 and j == 0)
)


def neighbours_silver(grid, x, y):
    return [
        grid.old_state(x + i, y + j)
        for i, j in DIRECTIONS
        if grid.inside_grid(x + i, y + j)
    ]


def neighbours_gold(grid, x, y):
    neighbours = []
    for i, j in DIRECTIONS:
        for multiplier in range(1, grid.height()):
            x_seen = x + i * multiplier
            y_seen = y + j * multiplier
            if not grid.inside_grid(x_seen, y_seen):
                break
            if grid.old_state(x_seen, y_seen) != ".":
                neighbours.append(grid.old_state(x_seen, y_seen))
                break
    return neighbours


@dataclass(frozen=True)
class Grid:
    grid: Tuple[str]
    neighbours_rule: Callable[["Grid", int, int], List[str]]
    seaters_tolerance: int

    @staticmethod
    def from_file(
            file_name: str,
            neighbours_rule: Callable[["Grid", int, int], List[str]] = neighbours_silver,
            seaters_tolerance: int = 4
    ):
        with open(file_name) as file:
            return Grid(tuple(file.read().split("\n")), neighbours_rule, seaters_tolerance)

    @lru_cache
    def width(self):
        return len(self.grid[0])

    @lru_cache
    def height(self):
        return len(self.grid)

    def tick(self, times=1):
        grid = self
        for _ in range(times):
            grid = grid.tick_once()
        return grid

    def tick_once(self):
        return Grid(
            tuple(
                "".join([
                    self.new_state(x, y)
                    for x in range(self.width())
                ])
                for y in range(self.height())
            ),
            self.neighbours_rule,
            self.seaters_tolerance,
        )

    def old_state(self, x, y):
        return self.grid[y][x]

    def new_state(self, x, y):
        if self.old_state(x, y) == "L" and self.neighbours(x, y).count("#") == 0:
            return "#"
        if self.old_state(x, y) == "#" and self.neighbours(x, y).count("#") >= self.seaters_tolerance:
            return "L"
        return self.old_state(x, y)

    def neighbours(self, x, y):
        return self.neighbours_rule(self, x, y)

    def inside_grid(self, x, y):
        return (
                0 <= x < self.width()
                and
                0 <= y < self.height()
        )

    def __repr__(self):
        return "\n" + "\n".join(self.grid) + "\n"

    def count(self, state):
        return str(self.grid).count(state)
