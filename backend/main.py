from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uuid
import os
from praisonai_core.dispatcher import Dispatcher

app = FastAPI(title="AppBuilder AI Backend")

PROJECTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'projects'))

# --- Экспорт в Notion ---
from praisonai_core.tools.mcp_notion_exporter.exporter import NotionExporter
import logging

class NotionExportRequest(BaseModel):
    api_token: str
    database_id: str
    export: str = "specification"  # specification|tasks|reports|all

@app.post("/projects/{project_id}/export_notion")
def export_to_notion(project_id: str, req: NotionExportRequest):
    """
    Экспортирует спецификацию, задачи и/или отчёты в Notion через MCP-агент.
    """
    exporter = NotionExporter(req.api_token, req.database_id)
    project_path = os.path.join(PROJECTS_PATH, project_id)
    results = {}
    if req.export in ("specification", "all"):
        spec_path = os.path.join(project_path, "specification.md")
        if os.path.exists(spec_path):
            with open(spec_path, "r", encoding="utf-8") as f:
                spec_md = f.read()
            try:
                results["specification"] = exporter.export_specification(spec_md, project_id)
            except Exception as e:
                logging.exception("Notion export (specification) failed")
                results["specification"] = str(e)
    if req.export in ("tasks", "all"):
        from praisonai_core.tools import context_manager
        state = context_manager.read_state(project_id)
        for task in state.get("tasks", []):
            try:
                results.setdefault("tasks", []).append(exporter.export_task(task))
            except Exception as e:
                logging.exception("Notion export (task) failed")
                results.setdefault("tasks", []).append(str(e))
    if req.export in ("reports", "all"):
        from praisonai_core.tools import context_manager
        state = context_manager.read_state(project_id)
        for report in state.get("reports", []):
            try:
                results.setdefault("reports", []).append(exporter.export_report(report))
            except Exception as e:
                logging.exception("Notion export (report) failed")
                results.setdefault("reports", []).append(str(e))
    return {"status": "notion_export_complete", "results": results}

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uuid
import os
from praisonai_core.dispatcher import Dispatcher

app = FastAPI(title="AppBuilder AI Backend")

PROJECTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'projects'))

class ProjectInitRequest(BaseModel):
    core_mandate: str

@app.post("/projects/init")
def init_project(req: ProjectInitRequest):
    project_id = str(uuid.uuid4())
    project_path = os.path.join(PROJECTS_PATH, project_id)
    os.makedirs(project_path, exist_ok=True)
    # Сохраняем core_mandate.txt
    with open(os.path.join(project_path, 'core_mandate.txt'), 'w', encoding='utf-8') as f:
        f.write(req.core_mandate)
    # Инициализируем пустые артефакты
    for fname in ['specification.md', 'adr_log.md', 'state.json']:
        with open(os.path.join(project_path, fname), 'w', encoding='utf-8') as f:
            if fname.endswith('.json'):
                f.write('{"status": "init", "tasks": [], "blockers": []}')
            else:
                f.write(f"# {fname}\n")
    os.makedirs(os.path.join(project_path, 'vector_store'), exist_ok=True)
    return {"project_id": project_id}


@app.post("/projects/{project_id}/run")
def run_project_workflow(project_id: str):
    dispatcher = Dispatcher(project_id)
    dispatcher.run_workflow()
    return {"status": "workflow_started"}

# --- Генерация документации ---
from praisonai_core.tools.doc_generator import generate_docs
from praisonai_core.tools.mcp_plane_exporter import export_docs_to_plane
from praisonai_core.tools.testing_runner import run_all_tests
from praisonai_core.tools.code_analyzer import run_brakeman
from praisonai_core.tools.test_generator import generate_tests
from praisonai_core.tools import context_manager
from fastapi import Body

@app.post("/projects/{project_id}/docs")
def generate_project_docs(project_id: str):
    context = context_manager.read_state(project_id)
    docs = generate_docs(project_id, str(context))
    # Сохраняем документацию в файл
    doc_path = os.path.join(PROJECTS_PATH, project_id, 'generated_docs.md')
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(docs)
    return {"status": "docs_generated", "path": doc_path}

@app.post("/projects/{project_id}/export_docs")
def export_project_docs(project_id: str, plane_api_token: str = Body(...), page_id: str = Body(None)):
    doc_path = os.path.join(PROJECTS_PATH, project_id, 'generated_docs.md')
    if not os.path.exists(doc_path):
        return {"error": "Docs not found. Generate first."}
    with open(doc_path, 'r', encoding='utf-8') as f:
        docs = f.read()
    url = export_docs_to_plane(project_id, docs, plane_api_token, page_id)
    return {"status": "exported", "url": url}

@app.post("/projects/{project_id}/run_tests")
def run_project_tests(project_id: str):
    from datetime import datetime
    project_path = os.path.join(PROJECTS_PATH, project_id)
    result = run_all_tests(project_path)
    # Определяем severity по наличию "failure"/"error" в выводе
    severity = "low"
    if result and ("failure" in result or "error" in result or "failed" in result):
        severity = "high"
    report = {
        "type": "qa_functional",
        "severity": severity,
        "content": result or "No output",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "related_task": None
    }
    context_manager.add_report(project_id, report)
    return {"status": "tests_run", "result": result, "report": report}

@app.post("/projects/{project_id}/security_audit")
def run_project_security_audit(project_id: str):
    from datetime import datetime
    project_path = os.path.join(PROJECTS_PATH, project_id)
    result = run_brakeman(project_path)
    # Определяем severity по наличию "warning"/"error"/"high" в выводе
    severity = "low"
    if result and ("high" in result or "error" in result or "warning" in result):
        severity = "high"
    report = {
        "type": "security_audit",
        "severity": severity,
        "content": result or "No output",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "related_task": None
    }
    context_manager.add_report(project_id, report)
    return {"status": "audit_run", "result": result, "report": report}

class FeedbackRequest(BaseModel):
    feedback: str

@app.post("/projects/{project_id}/feedback")
def submit_feedback(project_id: str, req: FeedbackRequest):
    # Создаём отчёт типа user_feedback и инициируем цикл доработки
    from datetime import datetime
    report = {
        "type": "user_feedback",
        "severity": "medium",
        "content": req.feedback,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "related_task": None
    }
    context_manager.add_report(project_id, report)
    # Инициируем correction cycle через Dispatcher
    dispatcher = Dispatcher(project_id)
    dispatcher.handle_correction_cycle()
    return {"status": "feedback_accepted", "report": report}

# --- Новый эндпоинт: статус и фильтрация задач/отчётов ---
@app.get("/projects/{project_id}/status")
def get_project_status(
    project_id: str,
    task_status: str = Query(None, description="Фильтр по статусу задачи"),
    report_type: str = Query(None, description="Фильтр по типу отчёта"),
    severity: str = Query(None, description="Фильтр по severity отчёта"),
    assigned_to: str = Query(None, description="Фильтр по исполнителю задачи")
):
    state = context_manager.read_state(project_id)
    tasks = state.get("tasks", [])
    reports = state.get("reports", [])
    # Фильтрация задач
    if task_status:
        tasks = [t for t in tasks if t.get("status") == task_status]
    if assigned_to:
        tasks = [t for t in tasks if t.get("assigned_to") == assigned_to]
    # Фильтрация отчётов
    if report_type:
        reports = [r for r in reports if r.get("type") == report_type]
    if severity:
        reports = [r for r in reports if r.get("severity") == severity]
    return {"status": state.get("status"), "tasks": tasks, "reports": reports}

# --- Новый эндпоинт: Live Project Context (весь state.json) ---
@app.get("/projects/{project_id}/context")
def get_project_context(project_id: str):
    state = context_manager.read_state(project_id)
    return state
