import unittest
from unittest.mock import patch
from praisonai_core.tools.doc_generator import generate_and_export_docs
from praisonai_core.tools import context_manager
import os

class TestDocGeneratorExport(unittest.TestCase):
    def setUp(self):
        self.project_id = "test_project_export"
        from praisonai_core.tools.context_manager import BASE_PROJECTS_PATH
        import shutil
        self.project_path = os.path.join(BASE_PROJECTS_PATH, self.project_id)
        if os.path.exists(self.project_path):
            shutil.rmtree(self.project_path)
        os.makedirs(self.project_path, exist_ok=True)
        self.state_path = os.path.join(self.project_path, 'state.json')
        state = {
            "id": self.project_id,
            "core_mandate": "test",
            "status": "init",
            "iteration_count": 0,
            "current_llm_cost": 0.0,
            "tasks": [],
            "reports": []
        }
        import json
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def tearDown(self):
        import shutil
        if os.path.exists(self.project_path):
            shutil.rmtree(self.project_path)

    @patch('praisonai_core.tools.mcp_plane_exporter.export_docs_to_plane')
    def test_generate_and_export_docs_success(self, mock_export):
        mock_export.return_value = "https://plane.so/page/123"
        url = generate_and_export_docs(self.project_id, "fake_token")
        self.assertTrue(url.startswith("http"))

    @patch('praisonai_core.tools.mcp_plane_exporter.export_docs_to_plane')
    def test_generate_and_export_docs_error(self, mock_export):
        mock_export.side_effect = Exception("Plane error")
        url = generate_and_export_docs(self.project_id, "fake_token")
        self.assertIn("Ошибка экспорта", url)

if __name__ == "__main__":
    unittest.main()
