from typing import List


def test_silver():
    entries = read_input()
    complements = {
        2020 - entry
        for entry in entries
    }
    matching = list(set(entries).intersection(complements))
    assert 786811 == matching[0] * matching[1]


def test_gold():
    entries = read_input()
    products = [
        entries[i1] * entries[i2] * entries[i3]
        for i1 in range(len(entries))
        for i2 in range(i1 + 1, len(entries))
        for i3 in range(i2 + 1, len(entries))
        if entries[i1] + entries[i2] + entries[i3] == 2020
    ]
    assert len(products) == 1
    assert 199068980 == products[0]


def read_input() -> List[int]:
    with open("input.txt") as file:
        entries = [
            int(line)
            for line in file.read().split("\n")
        ]
    return entries
