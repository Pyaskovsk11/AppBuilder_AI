import unittest
from praisonai_core.tools.doc_generator import generate_docs
from praisonai_core.tools.test_generator import generate_tests

class TestDocAndTestGenerator(unittest.TestCase):
    def test_generate_docs(self):
        doc = generate_docs("project-1", "{\"status\": \"in_progress\"}")
        self.assertIn("документация", doc.lower())

    def test_generate_tests(self):
        tests = generate_tests("project-1", "spec")
        self.assertIn("тест", tests.lower())

if __name__ == "__main__":
    unittest.main()
