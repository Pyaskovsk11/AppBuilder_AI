"""
MCP-агент для экспорта данных в Notion: спецификация, задачи, отчёты.
"""
from .notion_client import NotionClient
from typing import Dict, Any, List

class NotionExporter:
    def __init__(self, api_token: str, database_id: str):
        self.client = NotionClient(api_token, database_id)

    def export_specification(self, spec_md: str, project_name: str) -> Dict[str, Any]:
        # Преобразуем markdown в Notion blocks (упрощённо: как plain text)
        properties = {
            "Name": {"title": [{"text": {"content": f"Спецификация: {project_name}"}}]}
        }
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"text": [{"type": "text", "text": {"content": spec_md}}]}
            }
        ]
        return self.client.create_page(properties, children)

    def export_task(self, task: dict) -> Dict[str, Any]:
        properties = {
            "Name": {"title": [{"text": {"content": f"Task: {task.get('description','')}"}}]},
            "Status": {"select": {"name": task.get("status", "pending")}},
            "Assigned": {"rich_text": [{"text": {"content": task.get("assigned_to", "")}}]}
        }
        return self.client.create_page(properties)

    def export_report(self, report: dict) -> Dict[str, Any]:
        properties = {
            "Name": {"title": [{"text": {"content": f"Report: {report.get('type','')}"}}]},
            "Severity": {"select": {"name": report.get("severity", "medium")}},
            "Content": {"rich_text": [{"text": {"content": report.get("content", "")}}]}
        }
        return self.client.create_page(properties)

    def sync_status(self, page_id: str, status: str):
        return self.client.update_page(page_id, {"Status": {"select": {"name": status}}})
