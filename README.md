# AppBuilder_AI
Create an intelligent platform,  that fully automates the process of transforming a user's business idea into a ready-to-deploy web application.

# AppBuilder AI — Документация и план развития

## Основные возможности
- Генерация кода (backend, frontend, миграции)
- Генерация и запуск тестов (RSpec, test-generator)
- Аудит безопасности (Brakeman, security-auditor)
- Self-Correction Cycle: автоматический цикл QA → Report → Auto-fixer → Developer → QA
- Vectorized Codebase Indexing: семантический поиск и навигация по коду
- LLM Cost Tracking and Limiting: учёт и лимит стоимости вызовов LLM
- Генерация документации (doc-generator)
- MCP-агент для выгрузки документации в Plane.so
- Управление задачами с приоритетами, зависимостями, вложенностью
- Автоматизация анализа и создания задач на исправление

## Примеры API

### Инициализация проекта
POST `/projects/init`
```json
{"core_mandate": "Описание бизнес-идеи"}
```

### Запуск workflow
POST `/projects/{project_id}/dispatch`
Ответ: `{ "status": "workflow_started" }`

### Генерация документации
POST `/projects/{project_id}/docs`
Ответ: `{ "status": "docs_generated", "path": "..." }`

### Экспорт документации в Plane.so
POST `/projects/{project_id}/export_docs`
Тело: `{ "plane_api_token": "...", "page_id": null }`

### Запуск тестов
POST `/projects/{project_id}/run_tests`

### Аудит безопасности
POST `/projects/{project_id}/security_audit`

### Обратная связь (Live Project Context)
POST `/projects/{project_id}/feedback`
```json
{"feedback": "Добавить поле 'телефон' в форму регистрации"}
```

## Тестирование

Для запуска unit-тестов:
```bash
python -m unittest discover -s backend/tests -p "test_*.py"
```

## Best practices
- Все инструменты расширяются через `/tools/` (test_generator, auto_fixer, doc_generator, mcp_plane_exporter)
- Агентов и их роли описывать декларативно в `agents.yaml`
- Использовать итеративные циклы и автоматизацию для повышения качества
- Поддерживать новые типы задач, отчётов, бизнес-метрик
- Интеграция с внешними платформами через MCP-агентов

---

## Следующие задачи
1. Доработка doc-generator: генерация структурированной документации по коду и API
2. Автоматизация экспорта документации в Plane.so (MCP-агент)
3. Интеграция и dockerization RSpec и Brakeman, автоматизация тестов и аудита
4. Реализация фронтенда (React + Tailwind CSS), визуализация статуса и отчётов
5. Расширение Live Project Context: поддержка feedback, новые типы отчётов
6. Покрытие ключевых модулей unit-тестами, ревью архитектуры и оптимизация кода
# AppBuilder AI v4.0

Интеллектуальная платформа для автоматизированной генерации, тестирования, аудита и документирования веб-приложений на основе бизнес-идеи пользователя.

## Ключевые возможности
- Итеративные циклы самокоррекции (Self-Correction Cycle)
- Расширяемый набор инструментов: генерация тестов, автофиксация кода, генерация документации
- Вложенные задачи, зависимости, приоритеты, назначение агентов
- Поддержка статусов задач: pending, in_progress, awaiting_review, completed, failed
- Автоматизация анализа отчётов (Brakeman, RSpec) и создание задач на исправление
- Векторный индекс кодовой базы для семантического поиска
- Учёт стоимости LLM и лимитов

## Пример структуры задачи (state.json)
```
{
  "id": "project-1",
  "status": "in_progress",
  "iteration_count": 0,
  "current_llm_cost": 0.0,
  "tasks": [
    {
      "id": "task-1",
      "agent": "backend-dev",
      "description": "Реализовать API для постов",
      "status": "pending",
      "priority": 1,
      "dependencies": [],
      "assigned_to": "backend-dev",
      "artifacts_produced": ["app/models/post.rb", "app/controllers/posts_controller.rb"],
      "subtasks": [
        {"id": "task-1.1", "description": "Создать модель Post", "status": "pending"}
      ]
    }
  ],
  "reports": [
    {
      "type": "qa_functional",
      "severity": "medium",
      "content": "Тесты не проходят для PostsController.",
      "created_at": "2025-08-06T12:00:00Z",
      "related_task": "task-1"
    }
  ]
}
```

## Новые инструменты и агенты
- `/tools/test_generator.py` — генерация тестов
- `/tools/auto_fixer.py` — автоматическое исправление кода
- `/tools/doc_generator.py` — генерация документации
- MCP-агент для выгрузки документации в Plane.so (см. задачи ниже)

## MCP-агент для выгрузки документации в Plane.so

Файл: `/tools/mcp_plane_exporter.py`

**Назначение:**
Позволяет выгружать актуальную документацию проекта (Live Project Context, спецификации, ADR, отчёты) в Plane.so через API.

**Пример использования:**
```python
from praisonai_core.tools.mcp_plane_exporter import export_docs_to_plane

plane_api_token = "<PLANE_SO_API_TOKEN>"
project_id = "example_project_id"
docs = "...сгенерированная документация..."
url = export_docs_to_plane(project_id, docs, plane_api_token)
print(f"Документация выгружена: {url}")
```

**Возможности:**
- Создание и обновление страниц в Plane.so
- Авторизация через API-токен
- Возврат ссылки на страницу или описание ошибки

**Рекомендация:**
Вызов MCP-агента рекомендуется интегрировать в workflow после генерации документации (doc-generator), чтобы всегда поддерживать актуальную версию знаний в Plane.so.

### Новые агенты:
- test-generator: генерация тестов (RSpec)
- auto-fixer: автоматическое исправление кода по отчётам
- doc-generator: генерация и обновление документации

## Расширяемость
- Добавление новых инструментов и агентов декларативно (agents.yaml)
- Поддержка новых типов задач, отчётов, бизнес-метрик

## Задачи для развития
- Реализовать MCP-агента, который выгружает актуальную документацию проекта (Live Project Context, спецификации, ADR, отчёты) в Plane.so через API.
  - Агент должен поддерживать авторизацию, обновление и создание страниц в Plane.so.
  - Интеграция должна быть расширяемой для других платформ (Notion, Confluence и др.)