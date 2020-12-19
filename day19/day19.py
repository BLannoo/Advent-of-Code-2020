import re
from typing import Callable, Dict


def test_silver_example():
    rules, messages = parse("example_silver.txt")
    assembler = create_silver_assembler(rules)
    assert "a" == assembler(4)
    assert "b" == assembler(5)
    assert "(ab|ba)" == assembler(3)
    assert "(aa|bb)" == assembler(2)
    assert "((aa|bb)(ab|ba)|(ab|ba)(aa|bb))" == assembler(1)
    assert "a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b" == assembler(0)
    assert 2 == count_matches(silver_matcher_factory(assembler), messages)


def test_silver():
    rules, messages = parse("input.txt")
    assembler = create_silver_assembler(rules)
    assert 265 == count_matches(silver_matcher_factory(assembler), messages)


def test_gold_example_with_silver_assembler():
    rules, messages = parse("example_gold.txt")
    assembler = create_silver_assembler(rules)
    assert 3 == count_matches(silver_matcher_factory(assembler), messages)


def test_gold_example_with_gold_assembler():
    rules, messages = parse("example_gold.txt")
    assembler = create_silver_assembler(rules)
    assert "((b(a(bb|ab)|b(a|b)(a|b))|a(bbb|a(bb|a(a|b))))b|(((aa|ab)a|bbb)b|((a|b)a|bb)aa)a)" == assembler(42)
    assert "(b(b(aba|baa)|a(b(ab|(a|b)a)|a(ba|ab)))|a(b((ab|(a|b)a)b|((a|b)a|bb)a)|a(bab|(ba|bb)a)))" == assembler(31)

    assert not gold_matcher_factory(assembler)("abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa")
    assert gold_matcher_factory(assembler)("bbabbbbaabaabba")
    assert gold_matcher_factory(assembler)("babbbbaabbbbbabbbbbbaabaaabaaa")
    assert gold_matcher_factory(assembler)("aaabbbbbbaaaabaababaabababbabaaabbababababaaa")
    assert gold_matcher_factory(assembler)("bbbbbbbaaaabbbbaaabbabaaa")
    assert gold_matcher_factory(assembler)("bbbababbbbaaaaaaaabbababaaababaabab")
    assert gold_matcher_factory(assembler)("ababaaaaaabaaab")
    assert gold_matcher_factory(assembler)("ababaaaaabbbaba")
    assert gold_matcher_factory(assembler)("baabbaaaabbaaaababbaababb")
    assert gold_matcher_factory(assembler)("abbbbabbbbaaaababbbbbbaaaababb")
    assert gold_matcher_factory(assembler)("aaaaabbaabaaaaababaa")
    assert gold_matcher_factory(assembler)("aaaabbaabbaaaaaaabbbabbbaaabbaabaaa")
    assert not gold_matcher_factory(assembler)("aaaabbaaaabbaaa")
    assert not gold_matcher_factory(assembler)("babaaabbbaaabaababbaabababaaab")
    assert gold_matcher_factory(assembler)("aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba")

    assert 12 == count_matches(gold_matcher_factory(assembler), messages)


def test_gold():
    rules, messages = parse("input.txt")
    assembler = create_silver_assembler(rules)
    assert 394 == count_matches(gold_matcher_factory(assembler), messages)


def gold_matcher_factory(assembler: Callable[[int], str]) -> Callable[[str], bool]:
    def matches_gold(message: str) -> bool:
        match_11 = matches_11(message)
        match_11_count = 0
        match_8 = matches_8(message)
        match_8_count = 0
        while match_8 or match_11:
            if match_11:
                message = match_11.group("rest")
                match_11_count += 1
            elif match_8:
                message = match_8.group("rest")
                match_8_count += 1
            match_11 = matches_11(message)
            match_8 = matches_8(message)
        return message == "" and match_8_count > 0 and match_11_count > 0

    def matches_8(message):
        return re.match(assembler(42) + "(?P<rest>.*)$", message)

    def matches_11(message):
        return re.match(assembler(42) + "(?P<rest>.*)" + assembler(31) + "$", message)

    return matches_gold


def silver_matcher_factory(assembler: Callable[[int], str]) -> Callable[[str], bool]:
    return lambda message: re.match(assembler(0) + "$", message) is not None


def count_matches(matcher: Callable[[str], bool], messages):
    return sum([
        1
        for message in messages
        if matcher(message)
    ])


def create_silver_assembler(rules: Dict[int, str]):
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
