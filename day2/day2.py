import re


def test_silver():
    assert 660 == valid_count(read_input(), silver)


def test_gold():
    assert 530 == valid_count(read_input(), gold)


def silver(line: str) -> bool:
    match = re.match(
        r"(?P<min>\d+)-(?P<max>\d+) (?P<char>\w): (?P<password>\w+)",
        line
    )
    return int(match.group("min")) <= match.group("password").count(match.group("char")) <= int(match.group("max"))


def gold(line: str) -> bool:
    match = re.match(r"(?P<first>\d+)-(?P<second>\d+) (?P<char>\w): (?P<password>\w+)", line)
    return (
            (match.group("password")[int(match.group("first")) - 1] == match.group("char"))
            ^
            (match.group("password")[int(match.group("second")) - 1] == match.group("char"))
    )


def valid_count(lines, rule):
    valid = [
        line
        for line in lines
        if rule(line)
    ]
    return len(valid)


def read_input():
    with open("input.txt") as file:
        return file.read().split("\n")
