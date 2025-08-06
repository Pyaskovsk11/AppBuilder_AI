"""
Notion API client wrapper для MCP-агента.
"""
import requests

class NotionClient:
    def __init__(self, api_token: str, database_id: str):
        self.api_token = api_token
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1/"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def create_page(self, properties: dict, children: list = None):
        url = self.base_url + "pages"
        data = {
            "parent": {"database_id": self.database_id},
            "properties": properties
        }
        if children:
            data["children"] = children
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_page(self, page_id: str, properties: dict):
        url = self.base_url + f"pages/{page_id}"
        data = {"properties": properties}
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search(self, query: str):
        url = self.base_url + "search"
        data = {"query": query}
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
