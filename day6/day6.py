def test_silver():
    with open("input.txt") as file:
        groups = file.read().split("\n\n")
    assert 6551 == sum([
        len(set(group.replace("\n", "")))
        for group in groups
    ])


def test_gold():
    with open("input.txt") as file:
        groups = file.read().split("\n\n")

    print()
    assert 3358 == sum([
        len(set.intersection(
            *(
                set(person)
                for person in group.split("\n")
            )
        ))
        for group in groups
    ])
