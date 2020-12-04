from copy import deepcopy

from pip._vendor.colorama import Fore, Style


def test_gold_example():
    global VISUAL
    VISUAL = ["" for _ in range(len(open("input.txt").read().split("\n")))]
    tree_count = tree_count_generator("example.txt")
    assert 336 == tree_count(1, 1) * tree_count(1, 3) * tree_count(1, 5) * tree_count(1, 7) * tree_count(2, 1)
    print("\n", "\n".join(VISUAL))


def test_silver():
    tree_count = tree_count_generator("input.txt")
    assert 254 == tree_count(steps_down=1, steps_right=3)


def test_gold():
    tree_count = tree_count_generator("input.txt")
    assert 1666768320 == tree_count(1, 1) * tree_count(1, 3) * tree_count(1, 5) * tree_count(1, 7) * tree_count(2, 1)


def tree_count_generator(file_name):
    def tree_count(steps_down, steps_right):
        with open(file_name) as file:
            grid = file.read().split("\n")
        height = len(grid)
        width = len(grid[0])
        locations = [
            (h, h * steps_right / steps_down % width)
            for h in range(0, height)
        ]
        visualize(grid, locations)
        return sum([
            1
            for location in locations
            if location[0] % steps_down == 0 and grid[location[0]][int(location[1])] == "#"
        ])

    return tree_count


def visualize(grid, locations):
    for location in locations:
        print_line = list(grid[location[0]])
        if location[1] % 1 == 0:
            print_line[int(location[1])] = Fore.RED + print_line[int(location[1])] + Style.RESET_ALL
        VISUAL[location[0]] += "\t\t" + "".join(print_line)
