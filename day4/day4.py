import re


def test_silver():
    assert 202 == valid_count("input.txt", validate_silver)


def test_example_gold_invalid():
    assert 0 == valid_count("example_gold_invalid.txt", validate_gold)


def test_example_gold_valid():
    assert 4 == valid_count("example_gold_valid.txt", validate_gold)


# 138 is too high: re.match does not require exact matches => add ^ and $ to the patterns
def test_gold():
    assert 137 == valid_count("input.txt", validate_gold)


def valid_count(file_name, validate):
    with open(file_name) as file:
        passports = file.read().split("\n\n")
    return sum([1 for passport in passports if validate(passport)])


def validate_silver(passport: str):
    fields = re.findall(
        r"(\w+):",
        passport
    )
    return len(
        {
            "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"
        }.difference(set(fields))
    ) == 0


RULES = {
    ("byr", lambda val: 1920 <= int(val) <= 2002),
    ("iyr", lambda val: 2010 <= int(val) <= 2020),
    ("eyr", lambda val: 2020 <= int(val) <= 2030),
    ("hgt", lambda val: validate_hgt(val)),
    ("hcl", lambda val: re.match(r"^#[0-9a-f]{6}$", val)),
    ("ecl", lambda val: val in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}),
    ("pid", lambda val: re.match(r"^\d{9}$", val)),
}


def validate_gold(passport: str):
    passport_cleaned = passport.replace('\n', ' ')
    for field, rule in RULES:
        match = re.match(
            f".*{field}:([a-zA-Z0-9#]+).*",
            passport_cleaned
        )
        if not (match and rule(match[1])):
            return False
    print(passport_cleaned)
    return True


def validate_hgt(val: str):
    return (
            (val[-2:] == "cm" and 150 <= int(val[:-2]) <= 193)
            or
            (val[-2:] == "in" and 59 <= int(val[:-2]) <= 76)
    )
