def test_silver_example():
    assert 127 == find_invalid(load("example.txt"), 5)


def test_silver():
    assert 144381670 == find_invalid(load("input.txt"), 25)


def test_gold_example():
    assert 62 == weakness(load("example.txt"), 5)


def test_gold():
    assert 20532569 == weakness(load("input.txt"), 25)


def weakness(numbers, preamble_length):
    goal = find_invalid(numbers, preamble_length)
    for i in range(len(numbers)):
        sum = 0
        j = i
        while sum < goal:
            sum += numbers[j]
            j += 1
        if sum == goal:
            weak_sequence = numbers[i:j]
            return min(weak_sequence) + max(weak_sequence)


def is_valid(numbers, i, preamble_length):
    number = numbers[i]
    preamble = set(numbers[i - preamble_length:i])
    preamble.discard(number / 2)
    complements = {
        number - n
        for n in preamble
    }
    return len(preamble.intersection(complements)) > 0


def find_invalid(numbers, preamble_length):
    i = preamble_length
    while is_valid(numbers, i, preamble_length):
        i += 1
    invalid_number = numbers[i]
    return invalid_number


def load(file_name):
    with open(file_name) as file:
        numbers = [
            int(line)
            for line in file.read().split("\n")
        ]
    return numbers
