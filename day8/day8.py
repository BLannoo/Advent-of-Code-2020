from dataclasses import dataclass


def test_silver_example():
    assert 5 == run_till_loop(read_instructions("example.txt"))[0]


def test_silver():
    assert 1548 == run_till_loop(read_instructions("input.txt"))[0]


def test_gold_example():
    assert 8 == run_till_loop(read_instructions("example.txt"), True)[0]


def test_gold():
    assert 1375 == run_till_loop(read_instructions("input.txt"), True)[0]


@dataclass(frozen=True)
class Instruction:
    description: str

    def execute(self):
        if self.operation() == "nop":
            return 1, 0
        if self.operation() == "acc":
            return 1, self.argument()
        assert self.operation() == "jmp"
        return self.argument(), 0

    def operation(self):
        return self.description[:3]

    def argument(self):
        return int(self.description[3:])


def read_instructions(file_name: str):
    with open(file_name) as file:
        instructions = [
            Instruction(line)
            for line in file.read().split("\n")
        ]
    return instructions


def run_till_loop(instructions, branching=False, next_pointer=0):
    pointers = [next_pointer]
    accumulator = 0
    while pointers[-1] not in pointers[:-2]:
        pointer_increment, accumulator_increment = instructions[pointers[-1]].execute()
        next_pointer = pointers[-1] + pointer_increment
        pointers.append(next_pointer)
        accumulator += accumulator_increment

        if next_pointer == len(instructions):
            return accumulator, next_pointer

        next_instruction = instructions[next_pointer]
        if branching and "acc" != next_instruction.operation():
            corrected_instructions = correct_instructions(instructions, next_pointer)
            branch_accumulator, final_pointer = run_till_loop(corrected_instructions, False, next_pointer)
            if final_pointer == len(instructions):
                return branch_accumulator + accumulator, final_pointer

    return accumulator, next_pointer


def correct_instructions(instructions, next_pointer):
    next_instruction = instructions[next_pointer]
    corrected_instructions = instructions.copy()
    if "nop" == next_instruction.operation():
        correction = "jmp"
    elif "jmp" == next_instruction.operation():
        correction = "nop"
    else:
        raise Exception(f"Invalid operation {next_instruction.operation()}")
    corrected_instructions[next_pointer] = Instruction(f"{correction} {next_instruction.argument()}")
    return corrected_instructions
