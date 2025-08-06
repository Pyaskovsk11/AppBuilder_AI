# Модуль запуска тестов

import subprocess
import os
from typing import Optional

def run_all_tests(project_path: str) -> Optional[str]:
    """
    Запускает все тесты RSpec для Rails-проекта через Docker.
    Возвращает stdout (отчёт) или None при ошибке.
    """
    try:
        docker_cmd = [
            'docker', 'run', '--rm', '-v', f'{project_path}:/app', '-w', '/app', 'ruby:3.2',
            'bash', '-c', 'bundle install && bundle exec rspec --format json'
        ]
        result = subprocess.run(docker_cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return None
