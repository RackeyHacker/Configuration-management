import unittest
import yaml
from config3 import evaluate_postfix, format_array, process_data  # Импортируем process_data

# Добавляем функцию для загрузки YAML-данных из строки
def load_yaml_from_string(yaml_data: str):
    try:
        # Обрабатываем YAML-данные из строки
        lines = yaml_data.splitlines()
        cleaned_lines = []
        comments = []

        for line_number, line in enumerate(lines):
            # Убираем часть строки, начиная с символа ';' для комментариев
            comment_split = line.split(';', 1)
            cleaned_lines.append(comment_split[0].rstrip())
            if len(comment_split) > 1:
                comments.append((line_number, comment_split[1].strip()))  # Сохраняем комментарии с номерами строк

        cleaned_yaml_data = '\n'.join(cleaned_lines)
        data_dict = yaml.safe_load(cleaned_yaml_data)
        return data_dict, comments

    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка синтаксиса YAML: {str(e)}")

# Теперь тесты

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
        data, comments = load_yaml_from_string(yaml_data)  # Используем функцию load_yaml_from_string
        expected_output = [
            "42 -> key1",
            "3.14 -> key2"
        ]
        output_lines = process_data(data, {}, comments)
        self.assertEqual(output_lines, expected_output)

    def test_yaml_array(self):
        yaml_data = """
        key1: [1,2,3]
        """
        data, comments = load_yaml_from_string(yaml_data)
        expected_output = [
            "array(1, 2, 3) -> key1"
        ]
        output_lines = process_data(data, {}, comments)
        self.assertEqual(output_lines, expected_output)
        
    def test_yaml_postfix_expression(self):
        yaml_data = """
        key1:
          expr: ["1", "2", "+"]
        """
        data, comments = load_yaml_from_string(yaml_data)
        expected_output = [
            "3 -> {. 1 2 + .}"
        ]
        output_lines = process_data(data, {}, comments)
        self.assertEqual(output_lines, expected_output)

if __name__ == "__main__":
    unittest.main()
