import unittest
from collections import deque
import re

OPERATORS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    'pow': lambda x, y: x ** y
}

def evaluate_postfix(expression: list, constants: dict) -> any:
    stack = deque()
    for token in expression:
        if isinstance(token, (int, float)):
            stack.append(token)
        elif isinstance(token, str) and token.isdigit():
            stack.append(int(token))
        elif token in constants:
            stack.append(constants[token])
        elif token in OPERATORS:
            try:
                b = stack.pop()
                a = stack.pop()
                result = OPERATORS[token](a, b)
                stack.append(result)
            except IndexError:
                raise ValueError("Недостаточно операндов для операции")
        else:
            raise ValueError(f"Неизвестная операция или константа '{token}'")
    if len(stack) != 1:
        raise ValueError("Ошибка в выражении: неверный остаток на стеке")
    return stack.pop()

def format_array(array: list) -> str:
    return "array(" + ", ".join(map(str, array)) + ")"

class TestProgram(unittest.TestCase):

    def test_evaluate_postfix_addition(self):
        result = evaluate_postfix([1, 2, '+'], {})
        self.assertEqual(result, 3)

    def test_evaluate_postfix_subtraction(self):
        result = evaluate_postfix([5, 3, '-'], {})
        self.assertEqual(result, 2)
    def test_format_array(self):
        formatted = format_array([1, 2, 3])
        self.assertEqual(formatted, "array(1, 2, 3)")

    def test_empty_array(self):
        formatted = format_array([])
        self.assertEqual(formatted, "array()")

    def test_string_expression(self):
        result = evaluate_postfix(['a', 'b', '+'], {'a': 1, 'b': 2})
        self.assertEqual(result, 3)

if __name__ == "__main__":
    unittest.main()
