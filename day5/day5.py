def test_example_silver():
    assert 567 == seat_id("BFFFBBFRRR")
    assert 119 == seat_id("FFFBBBFRRR")
    assert 820 == seat_id("BBFFBBFRLL")


def test_silver():
    with open("input.txt") as file:
        seats = file.read().split("\n")

    assert 842 == max([seat_id(seat) for seat in seats])


def test_gold():
    with open("input.txt") as file:
        seats = file.read().split("\n")

    seat_ids = sorted([seat_id(seat) for seat in seats])
    your_seat = seat_ids[
                    [
                        seat_ids[i + 1] - seat_ids[i]
                        for i in range(len(seat_ids) - 1)
                    ].index(2)
                ] + 1
    assert your_seat not in seat_ids
    assert your_seat - 1 in seat_ids
    assert your_seat + 1 in seat_ids
    assert 617 == your_seat


def seat_id(seat):
    return int(
        seat.replace(
            "F", "0"
        ).replace(
            "B", "1"
        ).replace(
            "L", "0"
        ).replace(
            "R", "1"
        ),
        2
    )
