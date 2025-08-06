import unittest
from praisonai_core.tools import context_manager
import os
import tempfile
import shutil
import pytest

class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.project_id = "test_project"
        # Используем BASE_PROJECTS_PATH из context_manager для абсолютного пути
        from praisonai_core.tools.context_manager import BASE_PROJECTS_PATH
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = os.path.join(self.temp_dir, self.project_id)
        os.makedirs(self.project_path, exist_ok=True)
        # Переопределяем BASE_PROJECTS_PATH для теста
        context_manager.BASE_PROJECTS_PATH = self.temp_dir
        self.state_path = os.path.join(self.project_path, 'state.json')
        # Гарантируем корректный state.json с нужными ключами
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
        shutil.rmtree(self.temp_dir)

    def test_read_write_state(self):
        state = context_manager.read_state(self.project_id)
        self.assertEqual(state['status'], 'init')
        state['status'] = 'in_progress'
        context_manager.write_state(self.project_id, state)
        state2 = context_manager.read_state(self.project_id)
        self.assertEqual(state2['status'], 'in_progress')

    def test_increment_iteration_count(self):
        context_manager.increment_iteration_count(self.project_id)
        state = context_manager.read_state(self.project_id)
        self.assertEqual(state['iteration_count'], 1)

    def test_add_llm_cost(self):
        context_manager.add_llm_cost(self.project_id, 1.5)
        state = context_manager.read_state(self.project_id)
        self.assertEqual(state['current_llm_cost'], 1.5)

    def test_add_and_get_tasks(self):
        project_id, temp_dir = setup_test_project()
        try:
            task = {"id": "t1", "type": "feature", "description": "Test feature"}
            context_manager.add_task(project_id, task)
            tasks = context_manager.get_tasks(project_id)
            self.assertTrue(any(t["id"] == "t1" for t in tasks))
            # Проверяем автогенерацию подзадач
            subtasks = [st for t in tasks if t["id"] == "t1" for st in t.get("subtasks", [])]
            self.assertTrue(any(st["type"] == "qa_functional" for st in subtasks))
            self.assertTrue(any(st["type"] == "security_audit" for st in subtasks))
        finally:
            teardown_test_project(temp_dir)

    def test_update_task_status(self):
        project_id, temp_dir = setup_test_project()
        try:
            task = {"id": "t2", "type": "bugfix", "description": "Test bugfix"}
            context_manager.add_task(project_id, task)
            context_manager.update_task_status(project_id, "t2", "completed")
            tasks = context_manager.get_tasks(project_id)
            self.assertTrue(any(t["id"] == "t2" and t["status"] == "completed" for t in tasks))
        finally:
            teardown_test_project(temp_dir)

    def test_add_report_and_increment_iteration(self):
        project_id, temp_dir = setup_test_project()
        try:
            report = {"type": "qa_functional", "content": "Test report"}
            context_manager.add_report(project_id, report)
            state = context_manager.read_state(project_id)
            self.assertTrue(any(r["type"] == "qa_functional" for r in state.get("reports", [])))
            context_manager.increment_iteration_count(project_id)
            state2 = context_manager.read_state(project_id)
            self.assertEqual(state2["iteration_count"], 1)
        finally:
            teardown_test_project(temp_dir)

    def test_add_llm_cost(self):
        project_id, temp_dir = setup_test_project()
        try:
            context_manager.add_llm_cost(project_id, 5.5)
            state = context_manager.read_state(project_id)
            self.assertEqual(state["current_llm_cost"], 5.5)
            context_manager.add_llm_cost(project_id, 2.5)
            state2 = context_manager.read_state(project_id)
            self.assertEqual(state2["current_llm_cost"], 8.0)
        finally:
            teardown_test_project(temp_dir)

def setup_test_project():
    temp_dir = tempfile.mkdtemp()
    project_id = "test_project"
    project_path = os.path.join(temp_dir, project_id)
    os.makedirs(project_path, exist_ok=True)
    # Переопределяем BASE_PROJECTS_PATH для теста
    context_manager.BASE_PROJECTS_PATH = temp_dir
    return project_id, temp_dir

def teardown_test_project(temp_dir):
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    unittest.main()
