import math


def test_silver():
    with open("input.txt") as file:
        origin = int(file.readline())
        busses = file.readline().split(",")

    print(origin)
    print(busses)

    earliest_bus = min(
        [
            (int(bus), int(bus) - origin % int(bus))
            for bus in busses
            if bus != "x"
        ],
        key=lambda x: x[1]
    )

    assert 410 == earliest_bus[0] * earliest_bus[1]


def gold(input_str: str) -> int:
    print()
    print(f"solving: {input_str}")
    busses = input_str.split(",")

    requirements = [
        (shift, int(bus_str))
        for shift, bus_str in enumerate(busses)
        if bus_str != "x"
    ]

    shift = requirements[0][1]
    cycle = requirements[0][1]

    for requirement in requirements[1:]:
        for i in range(1_000):
            potential_shift = shift + cycle * i
            position = potential_shift + requirement[0]
            expected = requirement[1]
            if position % expected == 0:
                shift = potential_shift
                cycle = math.lcm(cycle, requirement[1])
                break

    return shift


def test_gold_example():
    assert 9 == gold("3,5")
    assert 3417 == gold("17,x,13,19")
    assert 754018 == gold("67,7,59,61")
    assert 779210 == gold("67,x,7,59,61")
    assert 1261476 == gold("67,7,x,59,61")
    assert 1202161486 == gold("1789,37,47,1889")


def test_gold():
    with open("input.txt") as file:
        _ = file.readline()
        busses = file.readline()

    assert 600691418730595 == gold(busses)
