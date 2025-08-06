# --- Векторизация и поиск по кодовой базе ---
from praisonai_core.tools import vector_store


def index_project_codebase(project_id: str, code_files: list[str]) -> None:
    """
    Индексирует указанные файлы проекта для семантического поиска.
    :param project_id: идентификатор проекта
    :param code_files: список файлов для индексации
    """
    vector_store.index_codebase(project_id, code_files)


def search_project_codebase(project_id: str, query: str) -> list[str]:
    """
    Выполняет семантический поиск по коду проекта.
    :param project_id: идентификатор проекта
    :param query: поисковый запрос
    :return: список релевантных файлов/фрагментов
    """
    return vector_store.search_codebase(project_id, query)
# Модуль управления Live Project Context

import os
import json
from typing import Any, Dict

BASE_PROJECTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../projects'))


def get_project_path(project_id: str) -> str:
    """
    Возвращает абсолютный путь к папке проекта.
    :param project_id: идентификатор проекта
    :return: путь к проекту
    """
    return os.path.join(BASE_PROJECTS_PATH, project_id)


def read_state(project_id: str) -> Dict[str, Any]:
    """
    Читает state.json проекта.
    :param project_id: идентификатор проекта
    :return: словарь состояния
    """
    path = os.path.join(get_project_path(project_id), 'state.json')
    if not os.path.exists(path):
        # Возвращаем дефолтное состояние, чтобы избежать KeyError
        return {'status': 'init'}
    with open(path, 'r', encoding='utf-8') as f:
        state = json.load(f)
    if 'status' not in state:
        state['status'] = 'init'
    return state


def write_state(project_id: str, state: Dict[str, Any]) -> None:
    """
    Записывает state.json проекта.
    :param project_id: идентификатор проекта
    :param state: новое состояние
    """
    path = os.path.join(get_project_path(project_id), 'state.json')
    # Гарантируем, что директория существует
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def read_specification(project_id: str) -> str:
    """
    Читает specification.md проекта.
    :param project_id: идентификатор проекта
    :return: содержимое спецификации
    """
    path = os.path.join(get_project_path(project_id), 'specification.md')
    if not os.path.exists(path):
        return ''
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def append_to_adr(project_id: str, adr_entry: str) -> None:
    """
    Добавляет запись в adr_log.md проекта.
    :param project_id: идентификатор проекта
    :param adr_entry: запись
    """
    path = os.path.join(get_project_path(project_id), 'adr_log.md')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"\n{adr_entry}\n")

# --- Новые функции для работы с расширенным state.json ---
from typing import List, Optional

def get_tasks(project_id: str) -> List[dict]:
    """
    Возвращает список задач проекта.
    :param project_id: идентификатор проекта
    :return: список задач
    """
    state = read_state(project_id)
    return state.get('tasks', [])

def add_task(project_id: str, task: dict) -> None:
    """
    Добавляет задачу в проект. Для задач типа 'feature' или 'bugfix' автоматически создаёт подзадачи на тесты и аудит.
    :param project_id: идентификатор проекта
    :param task: словарь с описанием задачи
    """
    state = read_state(project_id)
    subtasks = task.get('subtasks', [])
    if task.get('type') in ('feature', 'bugfix'):
        subtasks.append({
            'id': f"test_{task.get('id')}",
            'description': f"Генерация и запуск тестов для {task.get('id')}",
            'status': 'pending',
            'type': 'qa_functional',
            'assigned_to': 'test_generator'
        })
        subtasks.append({
            'id': f"audit_{task.get('id')}",
            'description': f"Аудит безопасности для {task.get('id')}",
            'status': 'pending',
            'type': 'security_audit',
            'assigned_to': 'security_auditor'
        })
        task['subtasks'] = subtasks
    state.setdefault('tasks', []).append(task)
    write_state(project_id, state)

def update_task_status(project_id: str, task_id: str, status: str) -> None:
    """
    Обновляет статус задачи по её идентификатору.
    :param project_id: идентификатор проекта
    :param task_id: идентификатор задачи
    :param status: новый статус
    """
    state = read_state(project_id)
    for task in state.get('tasks', []):
        if task['id'] == task_id:
            task['status'] = status
    write_state(project_id, state)

def add_report(project_id: str, report: dict) -> None:
    """
    Добавляет отчёт в проект.
    :param project_id: идентификатор проекта
    :param report: словарь с отчётом
    """
    state = read_state(project_id)
    state.setdefault('reports', []).append(report)
    write_state(project_id, state)

def increment_iteration_count(project_id: str) -> None:
    """
    Увеличивает счётчик итераций проекта.
    :param project_id: идентификатор проекта
    """
    state = read_state(project_id)
    state['iteration_count'] = state.get('iteration_count', 0) + 1
    write_state(project_id, state)

def add_llm_cost(project_id: str, cost: float) -> None:
    """
    Добавляет стоимость LLM к проекту.
    :param project_id: идентификатор проекта
    :param cost: добавляемая стоимость
    """
    state = read_state(project_id)
    state['current_llm_cost'] = state.get('current_llm_cost', 0.0) + cost
    write_state(project_id, state)
