import re
from typing import Callable, Dict


def test_silver_example():
    rules, messages = parse("example.txt")
    assert "a" == create_assembler(rules)(4)
    assert "b" == create_assembler(rules)(5)
    assert "(ab|ba)" == create_assembler(rules)(3)
    assert "(aa|bb)" == create_assembler(rules)(2)
    assert "((aa|bb)(ab|ba)|(ab|ba)(aa|bb))" == create_assembler(rules)(1)
    assert "a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b" == create_assembler(rules)(0)
    assert 2 == count_matches(rules, messages)


def test_silver():
    rules, messages = parse("input.txt")
    assert 265 == count_matches(rules, messages)


def count_matches(rules, messages):
    return sum([
        1
        for message in messages
        if re.match(create_assembler(rules)(0) + "$", message)
    ])


def create_assembler(rules: Dict[int, str]):

    rules_memory = {}

    def assemble(rule_id: int) -> str:
        current_rule = rules[rule_id]
        if "\"" in current_rule:
            rules_memory[rule_id] = current_rule[1]
        elif "|" in current_rule:
            option_a, option_b = current_rule.split(" | ")
            rules_memory[rule_id] = (
                    "(" +
                    assemble_simple_sequence(assemble, option_a) +
                    "|" +
                    assemble_simple_sequence(assemble, option_b) +
                    ")"
            )
        else:
            rules_memory[rule_id] = assemble_simple_sequence(assemble, current_rule)
        return rules_memory[rule_id]

    return assemble


def assemble_simple_sequence(assembler: Callable[[int], str], sequence: str):
    return "".join([
        assembler(int(number))
        for number in sequence.split(" ")
    ])


def parse(file_name):
    with open(file_name) as file:
        file_content = file.read()
        rules_desc, messages_desc = file_content.split("\n\n")
        rules = {
            int(rule_match.group(1)): rule_match.group(2)
            for rule_match in map(
                lambda rule_desc: re.match(r"^(\d+): (.*)$", rule_desc),
                rules_desc.split("\n")
            )
        }
        messages = messages_desc.split("\n")
    return rules, messages
