# MCP Notion Exporter

Агент для экспорта спецификации, задач и отчётов из AppBuilder AI в Notion через Notion API.

## Возможности
- Экспорт спецификации проекта (markdown → Notion page)
- Экспорт задач (Task) и отчётов (Report) в виде отдельных страниц
- Синхронизация статусов задач между AppBuilder AI и Notion
- Гибкая настройка шаблонов и маппинга данных

## Использование
1. Получите интеграционный токен Notion и ID базы данных.
2. Используйте `NotionExporter` для вызова методов:
   - `export_specification(spec_md, project_name)`
   - `export_task(task_dict)`
   - `export_report(report_dict)`
   - `sync_status(page_id, status)`

## Пример кода
```python
from praisonai_core.tools.mcp_notion_exporter.exporter import NotionExporter
exporter = NotionExporter(api_token="...", database_id="...")
exporter.export_specification("# Спецификация...", "MyProject")
```

## Требования
- Python requests
- Notion API integration

## TODO
- Улучшить парсинг markdown → Notion blocks
- Поддержка вложенных задач и связей
- Расширить шаблоны для отчётов и задач
