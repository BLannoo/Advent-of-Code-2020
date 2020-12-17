from functools import lru_cache
from typing import Set, Tuple


def projection(x, y, dim):
    loc = [0] * dim
    loc[0] = x
    loc[1] = y
    return tuple(loc)


def parse(description: str, dim=3):
    grid = description.strip().split("\n")
    return {
        projection(j, i, dim)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "#"
    }


FLAT_BLOCK_PATTERN = {(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)}
EXAMPLE = """
.#.
..#
###
"""
INPUT = """
#...#.#.
..#.#.##
..#..#..
.....###
...#.#.#
#.#.##..
#####...
.#.#.##.
"""


def test_1_cell_dies():
    assert tick_once({(0, 0, 0)}) == set()


def test_block_stays():
    assert tick(FLAT_BLOCK_PATTERN) == FLAT_BLOCK_PATTERN


def test_silver_example():
    assert 112 == len(tick(parse(EXAMPLE), 6))


def test_silver():
    assert 401 == len(tick(parse(INPUT), 6))


def test_gold_example():
    assert 848 == len(tick(parse(EXAMPLE, 4), 6))


def test_gold():
    assert 2224 == len(tick(parse(INPUT, 4), 6))


def render(universe: Set[Tuple[int, int, int]]):
    print()
    xs = range(min(universe, key=lambda loc: loc[0])[0], max(universe, key=lambda loc: loc[0])[0] + 1)
    ys = range(min(universe, key=lambda loc: loc[1])[1], max(universe, key=lambda loc: loc[1])[1] + 1)
    zs = range(min(universe, key=lambda loc: loc[2])[2], max(universe, key=lambda loc: loc[2])[2] + 1)
    for z in zs:
        print(f"\nz={z}\n {''.join([str(y)[-1] for y in xs])}")
        for y in ys:
            print(str(y)[-1], end="")
            for x in xs:
                if (x, y, z) in universe:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


def tick(old_universe, iterations=1):
    for iteration in range(iterations):
        old_universe = tick_once(old_universe)
        print(f"{iteration=}")
        render(old_universe)
    return old_universe


def tick_once(old_universe):
    new_universe = apply_rules(old_universe)
    return {
        cell
        for cell in potential_living_cells(old_universe)
        if new_universe(cell)
    }


def apply_rules(old_universe):
    def new_universe(location):
        neighbouring_locations = generate_neighbouring_locations(location)
        number_of_living_neighbours = len(neighbouring_locations.intersection(old_universe))
        return (
                (number_of_living_neighbours in (2, 3) and location in old_universe)
                or
                (number_of_living_neighbours == 3)
        )

    return new_universe


def potential_living_cells(old_universe):
    return {
        position
        for living_cell in old_universe
        for position in generate_neighbouring_locations(living_cell)
    }.union(old_universe)


def generate_neighbouring_locations(location: Tuple[int]):
    return {
        tuple(
            loc + delta[i]
            for i, loc in enumerate(location)
        )
        for delta in (generate_deltas(len(location)))
    }


@lru_cache()
def generate_deltas(total_dim):
    deltas = {(-1,), (0,), (1,)}
    for dim in range(1, total_dim):
        deltas = {
            high_dim_delta
            for low_dim_delta in deltas
            for high_dim_delta in {
                (*low_dim_delta, -1),
                (*low_dim_delta, 0),
                (*low_dim_delta, 1),
            }
        }
    deltas.remove((0,) * total_dim)
    return deltas
