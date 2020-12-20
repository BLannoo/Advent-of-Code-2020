from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple, Set


def test_gold_example():
    picture = load("example_picture.txt")
    assert Coordinates(0, 1) in to_coordinates(SEA_MONSTER)
    assert Coordinates(0, 0) not in to_coordinates(SEA_MONSTER)
    assert (20, 3) == measure(SEA_MONSTER)

    assert 0 == len(picture.find(SEA_MONSTER))

    picture_website_oriented = picture.flip_horizontally().rotate_right().rotate_right()
    assert load("example_picture_website.txt") == picture_website_oriented
    locations = picture_website_oriented.find(SEA_MONSTER)
    assert 2 == len(locations)

    assert 273 == picture_website_oriented.count_roughness(SEA_MONSTER)

    assert 273 == min(picture.find_any_orientation(SEA_MONSTER))


def test_gold():
    picture = load("input_picture.txt")
    assert 1939 == min(picture.find_any_orientation(SEA_MONSTER))


SEA_MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip("\n")


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int


def to_coordinates(picture: str) -> Set[Coordinates]:
    return {
        Coordinates(x, y)
        for y, line in enumerate(picture.split("\n"))
        for x, char in enumerate(line)
        if char == "#"
    }


def measure(picture: str) -> Tuple[int, int]:
    split = picture.split("\n")
    return len(split[0]), len(split)


def load(file_name):
    with open(file_name) as file:
        picture = Picture.create(file.read().strip("\n"))

    return picture


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
class Picture:
    pattern: Tuple[Tuple[str, ...], ...]

    def __repr__(self):
        return "\n".join(
            "".join(
                cell
                for cell in line
            )
            for line in self.pattern
        )

    def size(self) -> int:
        return len(self.pattern)

    @classmethod
    def create(cls, description: str) -> "Picture":
        return Picture(
            tuple(
                tuple(line)
                for line in description.split("\n")
            ),
        )

    def flip_horizontally(self) -> "Picture":
        return Picture(self.pattern[::-1])

    @lru_cache
    def rotate_right(self) -> "Picture":
        return Picture(
            tuple(
                tuple(
                    self.pattern[-x - 1][y]
                    for x in range(self.size())
                )
                for y in range(self.size())
            ),
        )

    @lru_cache
    def re_orient(self, orientation: Orientation) -> "Tile":
        re_oriented_tile = self
        if orientation.flip:
            re_oriented_tile = re_oriented_tile.flip_horizontally()
        for _ in range(orientation.right_rotations):
            re_oriented_tile = re_oriented_tile.rotate_right()
        return re_oriented_tile

    def find(self, target: str) -> Set[Coordinates]:
        target_size_x, target_size_y = measure(target)
        coords = to_coordinates(target)
        return {
            Coordinates(x, y)
            for x in range(self.size() - target_size_x)
            for y in range(self.size() - target_size_y)
            if all(
                self.pattern[coord.x + x][coord.y + y] == "#"
                for coord in coords
            )
        }

    def count_roughness(self, target: str) -> int:
        locations = self.find(target)
        return str(self).count("#") - len(locations) * target.count("#")

    def find_any_orientation(self, target: str):
        return {
            self.re_orient(orientation).count_roughness(target)
            for orientation in ALL_ORIENTATIONS
        }
