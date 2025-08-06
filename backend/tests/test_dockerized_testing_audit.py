import unittest
from praisonai_core.tools.testing_runner import run_all_tests
from praisonai_core.tools.code_analyzer import run_brakeman
import os

class TestDockerizedTestingAudit(unittest.TestCase):
    def test_run_all_tests_docker_stub(self):
        # Проверяем, что функция возвращает строку или None (docker stub)
        result = run_all_tests(os.getcwd())
        self.assertTrue(isinstance(result, str) or result is None)

    def test_run_brakeman_docker_stub(self):
        # Проверяем, что функция возвращает строку или None (docker stub)
        result = run_brakeman(os.getcwd())
        self.assertTrue(isinstance(result, str) or result is None)

if __name__ == "__main__":
    unittest.main()
