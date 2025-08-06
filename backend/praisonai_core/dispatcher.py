# PraisonAI Dispatcher Core
# Управляет последовательностью агентов, циклами контроля и эскалацией

from typing import Any, Dict


class Dispatcher:
    """
    Ядро управления жизненным циклом проекта:
    - Запускает агентов в нужной последовательности
    - Следит за статусом и блокировками (state.json)
    - Управляет циклами исправлений и эскалацией
    """

    def __init__(self, project_id: str) -> None:
        """
        :param project_id: идентификатор проекта
        """
        self.project_id: str = project_id
        self.state: dict = self.load_state()



    def load_state(self) -> Dict[str, Any]:
        """
        Загружает state.json проекта через context_manager.
        :return: состояние проекта
        """
        try:
            from praisonai_core.tools import context_manager
            return context_manager.read_state(self.project_id)
        except Exception as e:
            print(f"[Dispatcher] Ошибка чтения state.json: {e}")
            return {"status": "init", "tasks": [], "blockers": []}



    def save_state(self) -> None:
        """
        Сохраняет state.json через context_manager.
        """
        try:
            from praisonai_core.tools import context_manager
            context_manager.write_state(self.project_id, self.state)
        except Exception as e:
            print(f"[Dispatcher] Ошибка сохранения state.json: {e}")


    def run_workflow(self) -> None:
        """
        Главная точка входа: запускает весь workflow проекта.
        Генерирует задачи для агентов, переводит проект в статус in_progress.
        """
        self._generate_initial_tasks()
        self.state['status'] = 'in_progress'
        self.save_state()
        # Шаг 1: Анализ и проектирование
        self.run_agent('uiux')
        self.run_agent('project-manager')
        self.run_agent('solution-architect')
        # Шаг 2: Генерация кода
        self.run_agent('database-architect')
        self.run_agent('backend-dev')
        self.run_agent('frontend-dev')
        # Шаг 3: Контроль качества и безопасности
        self.run_agent('lead-qa')
        self.run_agent('security-auditor')
        # Шаг 4: Финализация
        self.run_agent('senior-devops')
        self.run_agent('doc-agent')
        # --- Интеграция MCP-агента Plane.so ---
        try:
            from praisonai_core.tools import doc_generator, mcp_plane_exporter
            # Собираем документацию (пример: Live Project Context)
            context = "..."  # Здесь можно собрать спецификацию, ADR, отчёты и т.д.
            docs = doc_generator.generate_docs(self.project_id, context)
            plane_api_token = "<PLANE_SO_API_TOKEN>"  # Заменить на реальный токен
            url = mcp_plane_exporter.export_docs_to_plane(self.project_id, docs, plane_api_token)
            print(f"[Dispatcher] Документация выгружена в Plane.so: {url}")
        except Exception as e:
            print(f"[Dispatcher] Ошибка выгрузки документации в Plane.so: {e}")
        self.state['status'] = 'completed'
        self.save_state()

    def _generate_initial_tasks(self):
        # Генерирует по одной задаче для каждого ключевого агента
        agents = [
            ('uiux', 'Создать дизайн и UX-описание'),
            ('project-manager', 'Сформировать техническую спецификацию'),
            ('solution-architect', 'Принять архитектурные решения'),
            ('database-architect', 'Сгенерировать миграции БД'),
            ('backend-dev', 'Реализовать backend-логику'),
            ('frontend-dev', 'Реализовать frontend-логику'),
            ('lead-qa', 'Запустить тесты'),
            ('security-auditor', 'Провести аудит безопасности'),
            ('senior-devops', 'Подготовить Dockerfile и docker-compose'),
            ('doc-agent', 'Сгенерировать документацию и LICENSE'),
        ]
        self.state['tasks'] = [
            {
                'agent': agent,
                'description': desc,
                'status': 'pending'
            } for agent, desc in agents
        ]


    def run_agent(self, agent_name: str):
        # Реальный вызов LLM/агента на основе agents.yaml
        print(f"[Dispatcher] Запуск агента: {agent_name}")
        task = self._get_next_task_for_agent(agent_name)
        if not task:
            print(f"[Dispatcher] Нет задач для агента '{agent_name}', задача пропущена.")
            self._mark_agent_status(agent_name, 'skipped')
            self.save_state()
            return
        print(f"[Dispatcher] Агенту '{agent_name}' назначена задача: {task}")
        self._mark_task_in_progress(task)
        self.state['last_agent'] = agent_name
        self.save_state()

        # --- Интеграция с agents.yaml ---
        agent_config = self._get_agent_config(agent_name)
        if not agent_config:
            print(f"[Dispatcher] Не найден конфиг агента '{agent_name}' в agents.yaml")
            self._mark_task_failed(task)
            self.save_state()
            return
        prompt = agent_config.get('role', '')
        model = agent_config.get('model', '')
        tools = agent_config.get('tools', [])
        print(f"[Dispatcher] PROMPT для агента '{agent_name}':\n{prompt}")
        print(f"[Dispatcher] Модель: {model}")
        print(f"[Dispatcher] Инструменты: {tools}")
        # Реальный вызов LLM (API)
        agent_result, agent_output = self._call_llm_agent(prompt, model, tools, task)
        if agent_result == 'done':
            self._mark_task_done(task)
            # Если агент должен записать результат — делаем это через context_manager
            self._handle_agent_output(agent_name, tools, agent_output)
        elif agent_result == 'failed':
            self._mark_task_failed(task)
            self.state['status'] = 'failed'
        else:
            self._mark_task_skipped(task)
        self.save_state()

    def _call_llm_agent(self, prompt, model, tools, task):
        """
        Универсальный вызов LLM через API с учётом стоимости. Возвращает ('done'|'failed'|'skipped', output)
        """
        import requests
        from praisonai_core.tools import context_manager
        # Проверка лимита стоимости
        llm_limit = 10.0  # Установить лимит (например, $10)
        current_cost = self.state.get('current_llm_cost', 0.0)
        if current_cost >= llm_limit:
            print(f"[Dispatcher] LLM cost limit reached: {current_cost} >= {llm_limit}")
            self.state['status'] = 'llm_cost_limit_exceeded'
            self.save_state()
            return 'failed', ''
        url = "https://api.example-llm.com/v1/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "task": task['description']
        }
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                output = data.get('result', '')
                # Учёт стоимости (пример: data['usage']['cost'])
                cost = float(data.get('usage', {}).get('cost', 0.01))
                context_manager.add_llm_cost(self.project_id, cost)
                self.state['current_llm_cost'] = self.state.get('current_llm_cost', 0.0) + cost
                return 'done', output
            else:
                print(f"[Dispatcher] LLM API error: {response.status_code} {response.text}")
                return 'failed', ''
        except Exception as e:
            print(f"[Dispatcher] Ошибка вызова LLM API: {e}")
            return 'failed', ''

    def _handle_agent_output(self, agent_name, tools, output):
        """
        Обработка вывода агента: если инструмент write_... есть — записываем результат в нужный файл через context_manager
        """
        from praisonai_core.tools import context_manager
        import os
        try:
            if not output:
                return
            # Пример: если агент может писать DESIGN.md
            if 'context_manager.write_design' in tools and agent_name == 'uiux':
                context_manager_path = context_manager.get_project_path(self.project_id)
                with open(os.path.join(context_manager_path, 'DESIGN.md'), 'w', encoding='utf-8') as f:
                    f.write(output)
            # Аналогично для других write_... инструментов (write_specification, append_to_adr и т.д.)
            if 'context_manager.write_specification' in tools and agent_name == 'project-manager':
                context_manager_path = context_manager.get_project_path(self.project_id)
                with open(os.path.join(context_manager_path, 'specification.md'), 'w', encoding='utf-8') as f:
                    f.write(output)
            if 'context_manager.append_to_adr' in tools and agent_name == 'solution-architect':
                context_manager.append_to_adr(self.project_id, output)
            # ...добавить обработку других инструментов по аналогии...
        except Exception as e:
            print(f"[Dispatcher] Ошибка обработки вывода агента: {e}")

    def _get_agent_config(self, agent_name: str):
        # Чтение agents.yaml и возврат конфига для агента
        import yaml
        import os
        agents_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'agents.yaml'))
        with open(agents_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('agents', {}).get(agent_name)

    def _simulate_agent_execution(self, agent_name, task):
        # Здесь будет реальный вызов LLM/агента. Сейчас — всегда успех.
        # Можно добавить логику имитации ошибок для теста.
        return 'done'

    def _mark_agent_status(self, agent_name, status):
        # Помечает все задачи агента определенным статусом, если нет задач
        for task in self.state.get('tasks', []):
            if task.get('agent') == agent_name and task.get('status') == 'pending':
                task['status'] = status

    def _mark_task_failed(self, task):
        task['status'] = 'failed'

    def _mark_task_skipped(self, task):
        task['status'] = 'skipped'

    def _get_next_task_for_agent(self, agent_name: str):
        # Возвращает первую задачу для агента из state.json
        tasks = self.state.get('tasks', [])
        for task in tasks:
            if task.get('agent') == agent_name and task.get('status') == 'pending':
                return task
        return None

    def _mark_task_in_progress(self, task):
        task['status'] = 'in_progress'

    def _mark_task_done(self, task):
        task['status'] = 'done'


    def handle_correction_cycle(self):
        # Автоматизация Self-Correction Cycle
        if self.state.get('status') in ('tests_failed', 'vulnerabilities_found'):
            print("[Dispatcher] Обнаружены ошибки — инициируем цикл исправления.")
            self.state['correction_cycle'] = self.state.get('correction_cycle', 0) + 1
            if self.state['correction_cycle'] > 3:
                self.state['status'] = 'human_intervention_required'
                self.save_state()
                return
            # Генерация задач на исправление по отчётам
            reports = self.state.get('reports', [])
            for report in reports:
                if report.get('type') in ('qa_functional', 'security_audit') and report.get('status') != 'fixed':
                    fix_task = {
                        'id': f"fix-{report.get('related_task', 'unknown')}-{self.state['correction_cycle']}",
                        'agent': 'auto-fixer',
                        'description': f"Исправить: {report.get('content', '')}",
                        'status': 'pending',
                        'priority': 1,
                        'dependencies': [report.get('related_task', '')],
                        'assigned_to': 'auto-fixer',
                        'artifacts_produced': [],
                        'subtasks': []
                    }
                    self.state.setdefault('tasks', []).append(fix_task)
                    report['status'] = 'fixed'  # помечаем отчёт как обработанный
            self.save_state()
            # Запуск auto-fixer и повторный цикл для developer/QA
            self.run_agent('auto-fixer')
            self.run_agent('backend-dev')
            self.run_agent('lead-qa')
