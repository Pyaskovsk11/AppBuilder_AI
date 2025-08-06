import unittest
from praisonai_core.tools.testing_runner import run_all_tests
from praisonai_core.tools.code_analyzer import run_brakeman
import os

class TestTestingAndAudit(unittest.TestCase):
    def test_run_all_tests_stub(self):
        # Тестируем, что функция возвращает строку или None (stub)
        result = run_all_tests(os.getcwd())
        self.assertTrue(isinstance(result, str) or result is None)

    def test_run_brakeman_stub(self):
        # Тестируем, что функция возвращает строку или None (stub)
        result = run_brakeman(os.getcwd())
        self.assertTrue(isinstance(result, str) or result is None)

if __name__ == "__main__":
    unittest.main()
