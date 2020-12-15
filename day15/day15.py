from typing import List


def solver(starting_numbers: List[int], turns: int) -> int:
    last_spoken = {
        number: i
        for i, number in enumerate(starting_numbers[:-1])
    }

    previous_number = starting_numbers[-1]

    for i in range(len(starting_numbers), turns):
        if previous_number in last_spoken:
            next_number = i - last_spoken[previous_number] - 1
            last_spoken[previous_number] = i - 1
            previous_number = next_number
        else:
            last_spoken[previous_number] = i - 1
            previous_number = 0

    return previous_number


def test_silver_example():
    assert 436 == solver([0, 3, 6], 2020)


def test_silver():
    assert 319 == solver([13, 16, 0, 12, 15, 1], 2020)


def test_gold():
    assert 2424 == solver([13, 16, 0, 12, 15, 1], 30_000_000)
