def test_silver_example():
    assert 8 == loop_size(5764801, 7)
    assert 11 == loop_size(17807724, 7)
    assert 14897079 == encryption_key(8, 17807724)
    assert 14897079 == encryption_key(11, 5764801)


def test_silver():
    assert 19924389 == encryption_key(loop_size(9717666, 7), 20089533)


def loop_size(public_key: int, subject_number: int) -> int:
    loops = 0
    value = 1
    while value != public_key:
        value *= subject_number
        value %= 20201227
        loops += 1
    return loops


def encryption_key(loops: int, subject_number: int) -> int:
    value = 1
    for _ in range(loops):
        value *= subject_number
        value %= 20201227
    return value
