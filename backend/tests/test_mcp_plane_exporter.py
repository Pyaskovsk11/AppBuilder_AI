import unittest
from praisonai_core.tools.mcp_plane_exporter import export_docs_to_plane

class TestMCPPlaneExporter(unittest.TestCase):
    def test_export_docs_to_plane_stub(self):
        # Проверяем, что функция возвращает строку (stub)
        url = export_docs_to_plane("project-1", "docs", "fake_token")
        self.assertIsInstance(url, str)

if __name__ == "__main__":
    unittest.main()
