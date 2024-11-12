import unittest
from collections import deque
from config3 import evaluate_postfix, format_array

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
