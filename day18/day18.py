def test_silver_example():
    print()
    assert 3 == evaluate("1 + 2")
    assert 71 == evaluate("1 + 2 * 3 + 4 * 5 + 6")
    assert 51 == evaluate("1 + (2 * 3) + (4 * (5 + 6))")


def test_silver():
    with open("input.txt") as file:
        expressions = file.read().split("\n")

    assert 29839238838303 == sum([evaluate(expression) for expression in expressions])


def evaluate(expression: str) -> int:
    print(expression)

    result = 0
    operation = "+"
    i = 0
    while i < len(expression):
        if expression[i].isdigit():
            j = find_end_of_number(expression, i)
            value = int(expression[i:j])
            result = execute(result, operation, value)
            i = j
        elif expression[i] in ["+", "*"]:
            operation = expression[i]
        elif expression[i] == "(":
            j = find_closing_brace(expression, i)
            sub_result = evaluate(expression[i + 1:j])
            result = execute(result, operation, sub_result)
            i = j
        i += 1
    return result


def find_end_of_number(expression, i):
    j = i
    while j < len(expression) and expression[j].isdigit():
        j += 1
    return j


def find_closing_brace(expression, i):
    assert expression[i] == "("
    open_braces = 1
    for j in range(i + 1, len(expression)):
        if expression[j] == "(":
            open_braces += 1
        elif expression[j] == ")":
            open_braces -= 1
            if open_braces == 0:
                break
    return j


def execute(result, operation, value):
    if operation == "+":
        result += value
    elif operation == "*":
        result *= value
    return result
