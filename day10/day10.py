import math
from typing import List


def test_silver_example():
    assert 35 == silver("example.txt")


# 1792 is too low
# 1856 is too low
def test_silver():
    assert 1885 == silver("input.txt")


def test_gold_example():
    assert 8 == gold("example.txt")


def test_gold():
    assert 2024782584832 == gold("input.txt")


def silver(file_name):
    jolt_levels = load_jolt_levels(file_name)

    differences = [
        jolt_levels[i + 1] - jolt_levels[i]
        for i in range(len(jolt_levels) - 1)
    ]

    assert 0 == sum([1 for diff in differences if diff > 3])
    return differences.count(1) * differences.count(3)


def gold(file_name):
    jolt_levels = load_jolt_levels(file_name)

    splits = [
        i
        for i in range(len(jolt_levels) - 1)
        if 3 == jolt_levels[i + 1] - jolt_levels[i]
    ]

    subsequences = [
        jolt_levels[splits[i] + 1:splits[i + 1] + 1]
        for i in range(len(splits) - 1)
    ]
    subsequences.append(jolt_levels[:splits[0] + 1])
    subsequences.append(jolt_levels[splits[-1] + 1:])

    return math.prod([
        count_paths(subsequence)
        for subsequence in subsequences
    ])


def load_jolt_levels(file_name):
    with open(file_name) as file:
        adapters = [
            int(line)
            for line in file.readlines()
        ]
    adapters.append(0)
    adapters.sort()
    adapters.append(adapters[-1] + 3)
    return adapters


def count_paths(subsequence: List[int]) -> int:
    if len(subsequence) == 1:
        return 1
    partial_paths = [[subsequence[0]]]
    full_paths = []
    while len(partial_paths) > 0:
        partial_path = partial_paths.pop()
        for step_size in [1, 2, 3]:
            next_step = partial_path[-1] + step_size
            suggested_path = partial_path.copy()
            suggested_path.append(next_step)
            if next_step == subsequence[-1]:
                full_paths.append(suggested_path)
            elif next_step in subsequence:
                partial_paths.append(suggested_path)
    return len(full_paths)
