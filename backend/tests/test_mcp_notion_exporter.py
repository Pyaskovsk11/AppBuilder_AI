import os
import pytest
from praisonai_core.tools.mcp_notion_exporter.exporter import NotionExporter

@pytest.mark.skip(reason="Тест требует валидный Notion API token и database_id")
def test_export_specification():
    api_token = os.environ.get("NOTION_API_TOKEN", "test-token")
    database_id = os.environ.get("NOTION_DATABASE_ID", "test-db")
    exporter = NotionExporter(api_token, database_id)
    result = exporter.export_specification("# Тестовая спецификация", "TestProject")
    assert "id" in result
