from dataclasses import dataclass
from typing import Tuple


def test_silver_example():
    cups = parse("389125467")

    assert Cycle((3, 8, 9, 1, 2, 5, 4, 6, 7), 0) == cups
    assert Cycle((3, 2, 8, 9, 1, 5, 4, 6, 7), 1) == (cups := cups.move())
    assert Cycle((3, 2, 5, 4, 6, 7, 8, 9, 1), 2) == (cups := cups.move())
    assert Cycle((7, 2, 5, 8, 9, 1, 3, 4, 6), 3) == (cups := cups.move())
    assert Cycle((3, 2, 5, 8, 4, 6, 7, 9, 1), 4) == (cups := cups.move())
    assert Cycle((9, 2, 5, 8, 4, 1, 3, 6, 7), 5) == (cups := cups.move())
    assert Cycle((7, 2, 5, 8, 4, 1, 9, 3, 6), 6) == (cups := cups.move())
    assert Cycle((8, 3, 6, 7, 4, 1, 9, 2, 5), 7) == (cups := cups.move())
    assert Cycle((7, 4, 1, 5, 8, 3, 9, 2, 6), 8) == (cups := cups.move())
    assert Cycle((5, 7, 4, 1, 8, 3, 9, 2, 6), 9) == (cups := cups.move())
    assert Cycle((5, 8, 3, 7, 4, 1, 9, 2, 6), 1) == (cups := cups.move())
    assert "92658374" == cups.silver()
    assert "67384529" == move(parse("389125467"), 100).silver()


def test_silver():
    assert "82934675" == move(parse("327465189"), 100).silver()


@dataclass(frozen=True)
class Cycle:
    values: Tuple[int, ...]
    current_cup_index: int

    def move(self):
        picked_up = self.values[self.current_cup_index + 1: self.current_cup_index + 4]
        print(f"{picked_up=}")
        rest = self.values[:self.current_cup_index + 1] + self.values[self.current_cup_index + 4:]
        destination = (self.values[self.current_cup_index] - 1 - 1) % len(self.values) + 1
        print(f"{destination}")
        while destination in picked_up:
            destination = (destination - 1 - 1) % len(self.values) + 1
        destination_location = rest.index(destination)
        new_values = rest[:destination_location + 1] + picked_up + rest[destination_location + 1:]

        if destination_location < self.current_cup_index:
            return Cycle(new_values, self.current_cup_index + 4).reset_cycle()
        else:
            return Cycle(new_values, self.current_cup_index + 1).reset_cycle()

    def __eq__(self, other: "Cycle") -> bool:
        return self.reset_cycle().values == other.reset_cycle().values

    def reset_cycle(self) -> "Cycle":
        return Cycle(self.values[self.current_cup_index:] + self.values[:self.current_cup_index], 0)

    def silver(self) -> str:
        return "".join(
            str(digit)
            for digit in self.values[self.values.index(1) + 1:] + self.values[:self.values.index(1)]
        )


def move(cups: Cycle, iterations: int) -> Cycle:
    for i in range(iterations):
        cups = cups.move()
    return cups


def parse(description: str) -> Cycle:
    return Cycle(tuple(int(digit) for digit in description), 0)
