import re
from typing import List


def alter_silver(value: int, mask: str):
    return int("".join(
        (f"{value:036b}"[i] if mask[i] == "X" else mask[i])
        for i in range(len(mask))
    ), 2)


def test_silver():
    with open("input.txt") as file:
        commands = file.read().split("\n")

    memory = {}

    for command in commands:
        match_mask = re.match(r"mask = ([01X]+)", command)
        if match_mask:
            mask = match_mask.group(1)

        match_mem = re.match(r"mem\[(\d+)] = (\d+)", command)
        if match_mem:
            address = match_mem.group(1)
            value = int(match_mem.group(2))

            memory[address] = alter_silver(value, mask)

    assert 6513443633260 == sum(memory.values())


def alter_gold(root_address: int, mask: str):
    masked_address = [
        (f"{root_address:036b}"[i] if mask[i] == "0" else mask[i])
        for i in range(len(mask))
    ]

    all_addresses = [masked_address]
    for i in range(len(masked_address)):
        if masked_address[i] == "X":
            all_addresses = [
                address[:i] + [variant] + address[i+1:]
                for address in all_addresses
                for variant in ["0", "1"]
            ]

    return [
        int("".join(address), 2)
        for address in all_addresses
    ]


def test_gold_example():
    assert [26, 27, 58, 59] == alter_gold(42, "000000000000000000000000000000X1001X")


def test_gold():
    with open("input.txt") as file:
        commands = file.read().split("\n")

    memory = {}

    for command in commands:
        match_mask = re.match(r"mask = ([01X]+)", command)
        if match_mask:
            mask = match_mask.group(1)

        match_mem = re.match(r"mem\[(\d+)] = (\d+)", command)
        if match_mem:
            root_address = int(match_mem.group(1))
            value = int(match_mem.group(2))

            for address in alter_gold(root_address, mask):
                memory[address] = value

    assert 3442819875191 == sum(memory.values())
