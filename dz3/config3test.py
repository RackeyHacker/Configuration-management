import unittest
import yaml
from collections import deque

OPERATORS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    'pow': lambda x, y: x ** y
}

def load_yaml(yaml_data: str):
    try:
        data = yaml.safe_load(yaml_data)
        comments = []
        return data, comments
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка синтаксиса YAML: {str(e)}")

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

def process_data(data: dict, constants: dict, comments: list) -> list:
    output_lines = []
    
    for key, value in data.items():
        if isinstance(value, (int, float)):
            output_lines.append(f"{value} -> {key}")
            constants[key] = value
        elif isinstance(value, list):
            output_lines.append(f"{format_array(value)} -> {key}")
            constants[key] = value
        elif isinstance(value, dict) and 'expr' in value:
            expr = value['expr']
            result = evaluate_postfix(expr, constants)
            expr_str = " ".join(str(x) for x in expr)
            output_lines.append(f"{{. {expr_str} .}} -> {key}")
            constants[key] = result
        else:
            raise ValueError(f"Некорректный формат для '{key}'")

        for comment in comments:
            output_lines[-1] += f" ; {comment}"
    
    return output_lines

def parse_yaml_to_config(yaml_data):
    data, comments = load_yaml(yaml_data)
    return process_data(data, {}, comments)

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

    def test_yaml_simple_numbers(self):
        yaml_data = """
        key1: 42
        key2: 3.14
        """
        expected_output = [
            "42 -> key1",
            "3.14 -> key2"
        ]
        self.assertEqual(parse_yaml_to_config(yaml_data), expected_output)

    def test_yaml_array(self):
        yaml_data = """
        key1: [1,2,3]
        """
        expected_output = [
            "array(1, 2, 3) -> key1"
        ]
        self.assertEqual(parse_yaml_to_config(yaml_data), expected_output)
        
    def test_yaml_postfix_expression(self):
        yaml_data = """
        key1:
          expr: ["1","2","+"]
        """
        expected_output = [
            "{. 1 2 + .} -> key1"
        ]
        self.assertEqual(parse_yaml_to_config(yaml_data), expected_output)


if __name__ == "__main__":
    unittest.main()
