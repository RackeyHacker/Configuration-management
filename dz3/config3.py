import yaml
import sys
import argparse
import re
from collections import deque
from typing import Any, Dict, List, Tuple

# Определение операций для вычислений
OPERATORS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    'pow': lambda x, y: x ** y
}

# Регулярное выражение для проверки корректности имён
NAME_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]*$'

def parse_arguments():
    parser = argparse.ArgumentParser(description="Конвертер YAML в учебный конфигурационный язык.")
    parser.add_argument("input", help="Путь к входному файлу.")
    parser.add_argument("output", help="Путь к выходному файлу.")
    return parser.parse_args()

def load_yaml(file_path: str) -> Tuple[Dict[str, Any], List[Tuple[int, str]]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        data, comments = remove_comments(data)
        data_dict = yaml.safe_load(data)
        return data_dict, comments
    except yaml.YAMLError as e:
        sys.stderr.write("Ошибка синтаксиса YAML: " + str(e) + "\n")
        sys.exit(1)
    except IOError as e:
        sys.stderr.write("Ошибка чтения файла: " + str(e) + "\n")
        sys.exit(1)

def remove_comments(data: str) -> Tuple[str, List[Tuple[int, str]]]:
    """Удаляет однострочные комментарии из данных и возвращает комментарии с их строками."""
    lines = data.splitlines()
    cleaned_lines = []
    comments = []
    
    for line_number, line in enumerate(lines):
        # Убираем часть строки, начиная с символа ';'
        comment_split = line.split(';', 1)
        cleaned_lines.append(comment_split[0].rstrip())
        if len(comment_split) > 1:
            comments.append((line_number, comment_split[1].strip()))  # Сохраняем номер строки и комментарий
    
    return '\n'.join(cleaned_lines), comments

def validate_name(name: str):
    if not re.match(NAME_REGEX, name):
        raise ValueError(f"Некорректное имя '{name}'")

def format_array(array: List[Any]) -> str:
    return "array(" + ", ".join(map(str, array)) + ")"

def evaluate_postfix(expression: List[Any], constants: Dict[str, Any]) -> Any:
    stack = deque()
    for token in expression:
        if isinstance(token, (int, float)):
            stack.append(token)
        elif isinstance(token, str) and token.isdigit():  # Обработка строковых чисел
            stack.append(int(token))  # Преобразуем строку в число
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

def format_postfix_expression(expression: List[str]) -> str:
    return "{. " + " ".join(expression) + " .}"

def process_data(data: Dict[str, Any], constants: Dict[str, Any], comments: List[Tuple[int, str]]) -> List[str]:
    output_lines = []
    
    # Словарь для сопоставления строковых номеров с комментариями
    comment_dict = {line_number: comment for line_number, comment in comments}
    
    for key, value in data.items():
        validate_name(key)
        output_line = ""
        
        if isinstance(value, (int, float)):  # Простое значение
            output_line = f"{value} -> {key}"
            constants[key] = value
        elif isinstance(value, list):  # Массив
            if all(isinstance(v, (int, float)) for v in value):
                output_line = f"{format_array(value)} -> {key}"
            else:
                raise ValueError(f"Массив '{key}' содержит недопустимые элементы")
        elif isinstance(value, dict) and "expr" in value:  # Постфиксное выражение
            expression = value["expr"]
            try:
                result = evaluate_postfix(expression, constants)
                postfix_expression = format_postfix_expression(expression)
                output_line = f"{result} -> {postfix_expression}"
                constants[key] = result
            except ValueError as e:
                raise ValueError(f"Ошибка в выражении для '{key}': {e}")
        else:
            raise ValueError(f"Некорректный формат для '{key}'")
        
        output_lines.append(output_line)

        # Добавляем комментарий, если есть соответствующий
        current_index = len(output_lines) - 1  # Индекс текущей строки вывода
        if current_index in comment_dict:
            output_lines[-1] += f"   ; {comment_dict[current_index]}"

    return output_lines

def main():
    args = parse_arguments()
    data, comments = load_yaml(args.input)
    constants = {}
    
    try:
        output_lines = process_data(data, constants, comments)
    except ValueError as e:
        sys.stderr.write("Ошибка обработки данных: " + str(e) + "\n")
        sys.exit(1)

    try:
        # Определяем максимальную длину строки вывода
        max_length = max(len(line) for line in output_lines)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            for line in output_lines:
                # Форматируем вывод с учетом максимальной длины
                formatted_line = f"{line:<{max_length}}".rstrip()  # Убираем лишние пробелы справа
                f.write(f"{formatted_line}\n")
    except IOError as e:
        sys.stderr.write("Ошибка записи в файл: " + str(e) + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
