def test_silver_example():
    print()
    assert 3 == silver("1 + 2")
    assert 71 == silver("1 + 2 * 3 + 4 * 5 + 6")
    assert 51 == silver("1 + (2 * 3) + (4 * (5 + 6))")


def test_silver():
    print()
    with open("input.txt") as file:
        expressions = file.read().split("\n")

    assert 29839238838303 == sum([silver(expression) for expression in expressions])


def test_gold_example():
    print()
    assert 7 == gold("1 + (2 * 3)")
    assert 9 == gold("1 + 2 * 3")
    assert 51 == gold("1 + (2 * 3) + (4 * (5 + 6))")
    assert 46 == gold("2 * 3 + (4 * 5)")


def test_gold():
    print()
    with open("input.txt") as file:
        expressions = file.read().split("\n")

    assert 201376568795521 == sum([gold(expression) for expression in expressions])


def gold(expression: str) -> int:
    while "(" in expression:
        print(expression)
        i = expression.find("(")
        j = find_closing_brace(expression, i)
        expression = expression[:i] + str(gold(expression[i + 1:j])) + expression[j + 1:]
    while "+" in expression:
        print(expression)
        expression = execute_operation(expression, "+")
    while "*" in expression:
        print(expression)
        expression = execute_operation(expression, "*")
    return int(expression)


def execute_operation(expression: str, operator: str) -> str:
    i = expression.find(operator)
    start = find_start_of_number(expression, end=i - 2)
    end = find_end_of_number(expression, start=i + 2)
    left = int(expression[start:i - 2 + 1])
    right = int(expression[i + 2:end + 1])
    val = eval(f"{left} {operator} {right}")
    expression = expression[:start] + " " + str(val) + expression[end + 1:]
    return expression


def silver(expression: str) -> int:
    print(expression)

    result = 0
    operation = "+"
    i = 0
    while i < len(expression):
        if expression[i].isdigit():
            j = find_end_of_number(expression, i)
            value = int(expression[i:j + 1])
            result = execute(result, operation, value)
            i = j + 1
        elif expression[i] in ["+", "*"]:
            operation = expression[i]
        elif expression[i] == "(":
            j = find_closing_brace(expression, i)
            sub_result = silver(expression[i + 1:j])
            result = execute(result, operation, sub_result)
            i = j
        i += 1
    return result


def find_end_of_number(expression, start):
    j = start
    while j < len(expression) and expression[j].isdigit():
        j += 1
    return j - 1


def find_start_of_number(expression, end):
    j = end
    while j > 0 and expression[j].isdigit():
        j -= 1
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
