from dataclasses import dataclass


def test_silver():
    assert 1645 == manhattan(execute_all(SilverFerry(), "input.txt"))


def test_gold():
    assert 35292 == manhattan(execute_all(GoldFerry(), "input.txt"))


@dataclass
class SilverFerry:
    x: int = 0
    y: int = 0
    dir: int = 0

    def execute_one(self, instruction: str):
        magnitude = int(instruction[1:])
        if instruction[0] == "N":
            self.y += magnitude
        elif instruction[0] == "S":
            self.y -= magnitude
        elif instruction[0] == "E":
            self.x += magnitude
        elif instruction[0] == "W":
            self.x -= magnitude
        elif instruction[0] == "L":
            self.dir = (self.dir + magnitude) % 360
        elif instruction[0] == "R":
            self.dir = (self.dir - magnitude) % 360
        elif instruction[0] == "F":
            if self.dir == 0:
                self.x += magnitude
            elif self.dir == 90:
                self.y += magnitude
            elif self.dir == 180:
                self.x -= magnitude
            elif self.dir == 270:
                self.y -= magnitude


@dataclass
class GoldFerry:
    x: int = 0
    y: int = 0
    waypoint_x: int = 10
    waypoint_y: int = 1

    def execute_one(self, instruction: str):
        magnitude = int(instruction[1:])
        if instruction[0] == "N":
            self.waypoint_y += magnitude
        elif instruction[0] == "S":
            self.waypoint_y -= magnitude
        elif instruction[0] == "E":
            self.waypoint_x += magnitude
        elif instruction[0] == "W":
            self.waypoint_x -= magnitude
        elif instruction[0] == "L":
            for _ in range(magnitude//90):
                self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x
        elif instruction[0] == "R":
            for _ in range(magnitude//90):
                self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x
        elif instruction[0] == "F":
            self.x += magnitude * self.waypoint_x
            self.y += magnitude * self.waypoint_y


def execute_all(ferry, file_name: str):
    with open(file_name) as file:
        instructions = file.read().split("\n")

    for instruction in instructions:
        ferry.execute_one(instruction)

    return ferry


def manhattan(ferry):
    return abs(ferry.x) + abs(ferry.y)
