import re
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple


def test_silver_example():
    assert 71 == scanning_error_rate("example_silver.txt")


def test_silver():
    assert 27802 == scanning_error_rate("input.txt")


def test_gold_example_silver():
    rules, your_ticket, nearby_tickets = parse("example_silver.txt")

    valid_tickets = filter_valid_tickets(nearby_tickets, rules)

    assert valid_tickets == [[7, 3, 47]]


def test_gold_example_gold():
    rules, your_ticket, nearby_tickets = parse("example_gold.txt")

    fields = match_fields(rules, nearby_tickets)

    assert fields == [(0, 'row'), (1, 'class'), (2, 'seat')]


def test_gold():
    rules, your_ticket, nearby_tickets = parse("input.txt")

    valid_tickets = filter_valid_tickets(nearby_tickets, rules)

    fields = match_fields(rules, valid_tickets)

    departure_fields = [
        field
        for field in fields
        if field[1].startswith("departure")
    ]

    assert 279139880759 == reduce(
        lambda x, y: x * y,
        [
            your_ticket[field[0]]
            for field in departure_fields
        ]
    )


@dataclass(frozen=True)
class Rule:
    field_name: str
    start_1: int
    end_1: int
    start_2: int
    end_2: int

    @staticmethod
    def parse(description):
        match = re.match(
            r"^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$",
            description
        )
        if not match:
            print(description)
        else:
            return Rule(
                field_name=match.group(1),
                start_1=int(match.group(2)),
                end_1=int(match.group(3)),
                start_2=int(match.group(4)),
                end_2=int(match.group(5)),
            )

    def valid(self, field):
        if self.start_1 <= field <= self.end_1:
            return True
        if self.start_2 <= field <= self.end_2:
            return True
        return False


def filter_valid_tickets(nearby_tickets, rules):
    return [
        nearby_ticket
        for nearby_ticket in nearby_tickets
        if all(
            valid(field, rules)
            for field in nearby_ticket
        )
    ]


def match_fields(rules: List[Rule], nearby_tickets):
    all = [
        rules
        for _ in rules
    ]

    for ticket in nearby_tickets:
        for i, field in enumerate(ticket):
            all[i] = [
                rule
                for rule in all[i]
                if rule.valid(field)
            ]

    matched_fields: List[Tuple[int, Rule]] = []

    while len(matched_fields) < len(rules):
        matched_fields.extend([
            (i, matching_rules[0])
            for i, matching_rules in enumerate(all)
            if len(matching_rules) == 1
        ])

        all = [
            list(set(matching_rules).difference({matched_field[1] for matched_field in matched_fields}))
            for matching_rules in all
        ]

    return [
        (i, rule.field_name)
        for i, rule in matched_fields
    ]


def parse(file_name):
    with open(file_name) as file:
        content = file.read()
    rules_section, your_ticket_section, nearby_tickets_section = content.split("\n\n")

    rules = [
        Rule.parse(description)
        for description in rules_section.split("\n")
    ]

    your_ticket = parse_ticket(your_ticket_section.split("\n")[1])

    nearby_tickets = [
        parse_ticket(nearby_ticket_str)
        for nearby_ticket_str in nearby_tickets_section.split("\n")[1:]
    ]

    return rules, your_ticket, nearby_tickets


def parse_ticket(ticket_str):
    return list(map(
        int,
        ticket_str.split(",")
    ))


def valid(field, rules: List[Rule]):
    for rule in rules:
        if rule.valid(field):
            return True
    return False


def scanning_error_rate(file_name):
    rules, your_ticket, nearby_tickets = parse(file_name)

    return sum([
        field
        for nearby_ticket in nearby_tickets
        for field in nearby_ticket
        if not valid(field, rules)
    ])
