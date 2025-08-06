def auto_export_docs_to_plane(project_id: str, plane_api_token: str, page_id: str = None) -> str:
    """
    Генерирует документацию и автоматически выгружает её в Plane.so.
    :param project_id: идентификатор проекта
    :param plane_api_token: токен API Plane.so
    :param page_id: id страницы (опционально)
    :return: ссылка на страницу или ошибка
    """
    from praisonai_core.tools.doc_generator import generate_docs
    from praisonai_core.tools import context_manager
    context = context_manager.read_state(project_id)
    docs = generate_docs(project_id, context)
    return export_docs_to_plane(project_id, docs, plane_api_token, page_id)
# MCP-агент для выгрузки документации в Plane.so
import requests

def export_docs_to_plane(project_id: str, docs: str, plane_api_token: str, page_id: str = None) -> str:
    """
    Выгружает документацию (docs) в Plane.so через API.
    Если page_id указан — обновляет страницу, иначе создаёт новую.
    Возвращает ссылку на страницу или ошибку.
    """
    url = "https://api.plane.so/v1/pages/"
    headers = {"Authorization": f"Bearer {plane_api_token}", "Content-Type": "application/json"}
    payload = {"title": f"Документация проекта {project_id}", "content": docs}
    if page_id:
        # Обновление существующей страницы
        url = url + page_id + "/"
        response = requests.patch(url, json=payload, headers=headers)
    else:
        # Создание новой страницы
        response = requests.post(url, json=payload, headers=headers)
    if response.status_code in (200, 201):
        data = response.json()
        return data.get("url", "")
    return f"Ошибка Plane.so: {response.status_code} {response.text}"
