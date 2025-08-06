import unittest
from praisonai_core.tools.doc_generator import generate_docs
from praisonai_core.tools.mcp_plane_exporter import auto_export_docs_to_plane
from praisonai_core.tools import context_manager
import os

class TestDocExportIntegration(unittest.TestCase):
    def setUp(self):
        self.project_id = "test_project_docs"
        self.project_path = os.path.join(os.path.dirname(__file__), '../../projects', self.project_id)
        os.makedirs(self.project_path, exist_ok=True)
        self.state_path = os.path.join(self.project_path, 'state.json')
        with open(self.state_path, 'w', encoding='utf-8') as f:
            f.write('{"status": "in_progress", "tasks": [], "reports": []}')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.project_path)

    def test_generate_docs(self):
        state = context_manager.read_state(self.project_id)
        doc = generate_docs(self.project_id, str(state))
        self.assertIn("Документация проекта", doc)
        self.assertIn("Модели данных", doc)

    def test_auto_export_docs_to_plane_stub(self):
        # Проверяем, что функция возвращает строку (stub, не реальный вызов API)
        url = auto_export_docs_to_plane(self.project_id, "fake_token")
        self.assertIsInstance(url, str)

if __name__ == "__main__":
    unittest.main()
