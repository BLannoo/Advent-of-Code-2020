from dataclasses import dataclass
from typing import Tuple, Optional, Union, Sequence


def test_silver_example():
    assert assemble("389125467").as_tuple() == (3, 8, 9, 1, 2, 5, 4, 6, 7,)
    assert assemble("389125467").find(1).as_tuple() == (1, 2, 5, 4, 6, 7, 3, 8, 9,)

    assert play_n(assemble("389125467"), 1, 9)[1].as_tuple() == (1, 5, 4, 6, 7, 3, 2, 8, 9,)
    assert play_n(assemble("389125467"), 2, 9)[1].as_tuple() == (1, 3, 2, 5, 4, 6, 7, 8, 9,)
    assert play_n(assemble("389125467"), 3, 9)[1].as_tuple() == (1, 3, 4, 6, 7, 2, 5, 8, 9,)
    assert play_n(assemble("389125467"), 4, 9)[1].as_tuple() == (1, 3, 2, 5, 8, 4, 6, 7, 9,)
    assert play_n(assemble("389125467"), 5, 9)[1].as_tuple() == (1, 3, 6, 7, 9, 2, 5, 8, 4,)
    assert play_n(assemble("389125467"), 6, 9)[1].as_tuple() == (1, 9, 3, 6, 7, 2, 5, 8, 4,)
    assert play_n(assemble("389125467"), 7, 9)[1].as_tuple() == (1, 9, 2, 5, 8, 3, 6, 7, 4,)
    assert play_n(assemble("389125467"), 8, 9)[1].as_tuple() == (1, 5, 8, 3, 9, 2, 6, 7, 4,)
    assert play_n(assemble("389125467"), 9, 9)[1].as_tuple() == (1, 8, 3, 9, 2, 6, 5, 7, 4,)
    assert play_n(assemble("389125467"), 10, 9)[1].as_tuple() == (1, 9, 2, 6, 5, 8, 3, 7, 4,)

    assert "67384529" == play_n(assemble("389125467"), number_of_rounds=100, number_of_cups=9)[1].silver()


def test_silver():
    assert "82934675" == play_n(assemble("327465189"), number_of_rounds=100, number_of_cups=9)[1].silver()


def test_gold_example():
    number_of_cups = 1_000_000
    number_of_rounds = 10_000_000
    current_cup = assemble("389125467")
    current_cup.add_extra_cups(number_of_cups)

    cup_1 = play_n(current_cup, number_of_rounds, number_of_cups)[1]
    assert cup_1.right.label == 934001
    assert cup_1.right.right.label == 159792
    assert cup_1.gold() == 149245887792


def test_gold():
    number_of_cups = 1_000_000
    number_of_rounds = 10_000_000
    current_cup = assemble("327465189")
    current_cup.add_extra_cups(number_of_cups)

    assert 474600314018 == play_n(current_cup, number_of_rounds, number_of_cups)[1].gold()


@dataclass
class Cup:
    label: int
    left: Optional["Cup"] = None
    right: Optional["Cup"] = None

    def add_to_right(self, right_cup: "Cup") -> None:
        right_cup.left = self
        self.right = right_cup

    def find(self, value: int) -> "Cup":
        cup = self
        while cup.label != value:
            cup = cup.right
        return cup

    def as_tuple(self) -> Tuple[int, ...]:
        result = [self.label]
        next_link = self.right
        while next_link != self and next_link is not None:
            result.append(next_link.label)
            next_link = next_link.right
        return tuple(result)

    def silver(self):
        return "".join(str(digit) for digit in self.as_tuple())[1:]

    def gold(self):
        cup_1 = self.find(1)
        return cup_1.right.label * cup_1.right.right.label

    def add_extra_cups(self, number_of_cups: int) -> None:
        last_cup = self.left
        first_extra_cup = assemble(list(range(10, number_of_cups + 1)))
        last_extra_cup = first_extra_cup.left
        last_extra_cup.add_to_right(self)
        last_cup.add_to_right(first_extra_cup)

    def generate_pointer_list(self, number_of_cups: int) -> Tuple["Cup", ...]:
        result = [self] * (number_of_cups + 1)
        next_link = self.right
        while next_link != self and next_link is not None:
            result[next_link.label] = next_link
            next_link = next_link.right
        return tuple(result)


def play_n(current_cup: Cup, number_of_rounds: int, number_of_cups: int) -> Tuple[Cup, ...]:
    pointer_list = current_cup.generate_pointer_list(number_of_cups)
    for _ in range(number_of_rounds):
        current_cup = play(current_cup, number_of_cups, pointer_list)
    return pointer_list


def play(current_cup: Cup, number_of_cups: int, pointer_list: Tuple[Cup, ...]) -> Cup:
    picked_up_first = current_cup.right
    picked_up_second = picked_up_first.right
    picked_up_last = picked_up_second.right
    picked_up = (picked_up_first.label, picked_up_second.label, picked_up_last.label)
    current_cup.add_to_right(picked_up_last.right)
    destination = (current_cup.label - 1 - 1) % number_of_cups + 1
    while destination in picked_up:
        destination = (destination - 1 - 1) % number_of_cups + 1
    target = pointer_list[destination]
    picked_up_last.add_to_right(target.right)
    target.add_to_right(picked_up_first)
    return current_cup.right


def assemble(description: Sequence[Union[str, int]]):
    first_cup = Cup(int(description[0]))
    last_cup = first_cup
    for digit in description[1:]:
        next_cup = Cup(int(digit))
        last_cup.add_to_right(next_cup)
        last_cup = next_cup
    last_cup.right = first_cup
    first_cup.left = last_cup
    return first_cup
