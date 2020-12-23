from typing import Tuple


def test_silver_example():
    player1, player2 = parse("example.txt")
    player1, player2 = silver(player1, player2)
    assert 306 == score(player1) + score(player2)


def test_silver():
    player1, player2 = parse("input.txt")
    player1, player2 = silver(player1, player2)
    assert 34324 == score(player1) + score(player2)


def test_gold_example():
    player1, player2 = parse("example.txt")
    player1, player2 = gold(player1, player2)
    assert player1 == tuple()
    assert player2 == (7, 5, 6, 2, 4, 1, 10, 8, 9, 3)
    assert 291 == score(player1) + score(player2)


def test_gold_infinite_game():
    player1 = (43, 19)
    player2 = (2, 29, 14)
    player1, player2 = gold(player1, player2)
    assert player1 == (43, 19)
    assert player2 == (2, 29, 14)
    assert 105 == score(player1)


def test_gold():
    player1, player2 = parse("input.txt")
    player1, player2 = gold(player1, player2)
    assert 33259 == score(player1) + score(player2)


def gold(
        player1_immutable: Tuple[int, ...],
        player2_immutable: Tuple[int, ...],
) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    player1 = list(player1_immutable)
    player2 = list(player2_immutable)
    print()
    games_played = set()
    while len(player1) > 0 and len(player2) > 0:
        game_record = (tuple(player1), tuple(player2))
        if game_record in games_played:
            return tuple(player1), tuple(player2)
        games_played.add(game_record)
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        if len(player1) >= card1 and len(player2) >= card2:
            player1_result, player2_result = gold(
                tuple(player1[:card1].copy()),
                tuple(player2[:card2].copy()),
            )
            if len(player1_result) == 0:
                player2.append(card2)
                player2.append(card1)
            else:
                player1.append(card1)
                player1.append(card2)
        elif card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)
    return tuple(player1), tuple(player2)


def silver(
        player1_immutable: Tuple[int, ...],
        player2_immutable: Tuple[int, ...],
) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    player1 = list(player1_immutable)
    player2 = list(player2_immutable)
    while len(player1) > 0 and len(player2) > 0:
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)
    return tuple(player1), tuple(player2)


def score(player):
    return sum([
        (i + 1) * card
        for i, card in enumerate(player[::-1])
    ])


def parse(file_name: str) -> Tuple[Tuple[int], Tuple[int]]:
    with open(file_name) as file:
        player1, player2 = file.read().split("\n\n")
        return (
            tuple(
                int(card)
                for card in player1.split("\n")[1:]
            ),
            tuple(
                int(card)
                for card in player2.split("\n")[1:]
            )
        )
