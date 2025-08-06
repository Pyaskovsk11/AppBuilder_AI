def generate_and_export_docs(project_id: str, plane_api_token: str, page_id: str = None) -> str:
    """
    Генерирует документацию и автоматически экспортирует её в Plane.so.
    :param project_id: идентификатор проекта
    :param plane_api_token: токен API Plane.so
    :param page_id: id страницы (опционально)
    :return: ссылка на страницу или ошибка
    """
    docs = generate_docs(project_id, None)
    try:
        from praisonai_core.tools.mcp_plane_exporter import export_docs_to_plane
        url = export_docs_to_plane(project_id, docs, plane_api_token, page_id)
        return url
    except Exception as e:
        return f"Ошибка экспорта в Plane.so: {e}"



import json
from typing import Any
from praisonai_core.tools import context_manager

def generate_docs(project_id: str, context: str) -> str:
    """
    Генерирует структурированную документацию по проекту.
    :param project_id: идентификатор проекта
    :param context: сериализованный Live Project Context (json или str)
    :return: markdown-документация
    """
    # Парсим context (state.json)
    try:
        state = json.loads(context)
    except Exception:
        state = context_manager.read_state(project_id)

    doc = f"# Документация проекта {project_id}\n\n"
    doc += "## Оглавление\n"
    doc += "1. [Архитектура](#архитектура)\n"
    doc += "2. [Workflow](#workflow)\n"
    doc += "3. [Модели данных](#модели-данных)\n"
    doc += "4. [Текущие задачи](#текущие-задачи)\n"
    doc += "5. [Последние отчёты](#последние-отчёты)\n"
    doc += "6. [API-эндпоинты](#api-эндпоинты)\n\n"

    doc += "## Архитектура\n"
    doc += "- FastAPI backend (Python)\n- PraisonAI Core (агенты, dispatcher, инструменты)\n- Live Project Context (единый источник правды)\n- Frontend (React, Tailwind CSS)\n- Redis (кэширование)\n- Docker-инфраструктура\n\n"

    doc += "## Workflow\n"
    doc += "- Итеративный Self-Correction Cycle: QA → Report → Auto-fixer → Developer → QA\n"
    doc += "- Автоматическая генерация задач на исправление по отчётам\n"
    doc += "- Векторизация кода для семантического поиска (vector_store)\n"
    doc += "- Учёт стоимости LLM, лимитирование\n\n"

    doc += "## Модели данных\n"
    doc += "### Project\n"
    doc += "- id: str\n- core_mandate: str\n- status: str\n- iteration_count: int\n- current_llm_cost: float\n- tasks: list\n- reports: list\n\n"
    doc += "### Task\n- id: str\n- agent: str\n- description: str\n- status: str\n- priority: int\n- dependencies: list\n- assigned_to: str\n- artifacts_produced: list\n- subtasks: list\n\n"
    doc += "### Report\n- type: str\n- severity: str\n- content: str\n- created_at: str\n- related_task: str\n\n"

    doc += "## Текущие задачи\n"
    for t in state.get('tasks', []):
        doc += f"- [{t.get('status')}] {t.get('description')} (id: {t.get('id')}, agent: {t.get('agent')})\n"
        if t.get('subtasks'):
            for st in t['subtasks']:
                doc += f"    - [{st.get('status')}] {st.get('description')} (id: {st.get('id')})\n"
    doc += "\n"

    doc += "## Последние отчёты\n"
    for r in state.get('reports', []):
        doc += f"- [{r.get('type')}] {r.get('content')} (severity: {r.get('severity')}, created_at: {r.get('created_at')})\n"
    doc += "\n"

    doc += "## API-эндпоинты\n"
    doc += "| Метод | URL | Описание | Пример запроса | Пример ответа |\n"
    doc += "|-------|-----|----------|---------------|---------------|\n"
    doc += "| POST  | /projects/init | Инициализация проекта | `{}` | `{\"status\": \"ok\"}` |\n"
    doc += "| POST  | /projects/{project_id}/dispatch | Запуск/продолжение workflow | `{}` | `{\"status\": \"workflow_started\"}` |\n"
    doc += "| GET   | /projects/{project_id}/status | Статус, задачи и отчёты | - | `{...}` |\n"
    doc += "| GET   | /projects/{project_id}/context | Live Project Context | - | `{...}` |\n"
    doc += "| POST  | /projects/{project_id}/feedback | Итеративная доработка | `{\"feedback\": \"Добавить поле 'телефон'\"}` | `{\"status\": \"feedback_accepted\", \"report_id\": \"report-2\"}` |\n"
    doc += "\n(Автоматически сгенерировано)\n"
    return doc
