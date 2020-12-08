import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, Set, Dict


@dataclass(frozen=True)
class Rule:
    rule_string: str

    def parent_bag(self) -> str:
        return self.rule_string.split(" bags contain ")[0]

    def child_bags(self) -> Set[Tuple[str, str]]:
        if " contain no other bags." in self.rule_string:
            return set()
        return {
            re.match(r"(\d+) (.*) bags?", child_bag_string.replace(".\n", "")).groups()
            for child_bag_string in self.rule_string.split(" bags contain ")[1].split(", ")
        }


def test_silver():
    assert 233 == len(get_ancestor_bags("shiny gold", invert_rules(parse_rules("input.txt"))))


def invert_rules(rules: Dict[str, Rule]) -> Dict[str, Set[str]]:
    inverted_rules = defaultdict(set)
    for rule in rules.values():
        for quantity, child_bag in rule.child_bags():
            inverted_rules[child_bag].add(rule.parent_bag())
    return inverted_rules


def parse_rules(file_name: str) -> Dict[str, Rule]:
    with open(file_name) as file:
        return {
            Rule(rule_string).parent_bag(): Rule(rule_string)
            for rule_string in file
        }


def get_ancestor_bags(child_bag: str, inverted_rules: Dict[str, Set[str]]) -> Set[str]:
    parent_bags = inverted_rules[child_bag]
    if parent_bags == set():
        return set()
    parents_ancestor_bags = (
        get_ancestor_bags(parent_bag, inverted_rules)
        for parent_bag in parent_bags
    )
    return set.union(parent_bags, *parents_ancestor_bags)


def test_example_gold():
    assert 126 == -1 + count_required_bags("shiny gold", parse_rules("example_gold.txt"))


# 300252 is too low, only counted the final children
# 421551 is too high, also counted the original "shiny gold" bag
def test_gold():
    assert 421550 == -1 + count_required_bags("shiny gold", parse_rules("input.txt"))


def count_required_bags(parent_bag: str, rules: Dict[str, Rule]) -> int:
    return 1 + sum((
        int(quantity) * count_required_bags(child_bag, rules)
        for quantity, child_bag in rules[parent_bag].child_bags()
    ))
