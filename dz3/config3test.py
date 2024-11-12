import unittest
from config3 import evaluate_postfix, format_array, process_data, load_yaml

class TestProgram(unittest.TestCase):

    def test_evaluate_postfix_addition(self):
        # Проверка работы операции сложения в постфиксной записи
        result = evaluate_postfix([1, 2, '+'], {})
        self.assertEqual(result, 3)

    def test_evaluate_postfix_subtraction(self):
        # Проверка работы операции вычитания в постфиксной записи
        result = evaluate_postfix([5, 3, '-'], {})
        self.assertEqual(result, 2)

    def test_format_array(self):
        # Проверка правильности форматирования массива
        formatted = format_array([1, 2, 3])
        self.assertEqual(formatted, "array(1, 2, 3)")

    def test_empty_array(self):
        # Проверка на пустой массив
        formatted = format_array([])
        self.assertEqual(formatted, "array()")

    def test_string_expression(self):
        # Проверка работы с постфиксными выражениями с переменными
        result = evaluate_postfix(['a', 'b', '+'], {'a': 1, 'b': 2})
        self.assertEqual(result, 3)

    def test_yaml_simple_numbers(self):
        # Тест для простых числовых данных в YAML
        yaml_data = """
        key1: 42
        key2: 3.14
        """
        expected_output = [
            "42 -> key1",
            "3.14 -> key2"
        ]
        # Используем функцию process_data для обработки YAML данных
        data, comments = load_yaml(yaml_data)
        self.assertEqual(process_data(data, {}, comments), expected_output)

    def test_yaml_array(self):
        # Тест для массива в YAML
        yaml_data = """
        key1: [1, 2, 3]
        """
        expected_output = [
            "array(1, 2, 3) -> key1"
        ]
        data, comments = load_yaml(yaml_data)
        self.assertEqual(process_data(data, {}, comments), expected_output)

    def test_yaml_postfix_expression(self):
        # Тест для выражений в постфиксной записи в YAML
        yaml_data = """
        key1:
          expr: ["1", "2", "+"]
        """
        expected_output = [
            "{. 1 2 + .} -> key1"
        ]
        data, comments = load_yaml(yaml_data)
        self.assertEqual(process_data(data, {}, comments), expected_output)


if __name__ == "__main__":
    unittest.main()
