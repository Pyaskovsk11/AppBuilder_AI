# AppBuilder AI

An intelligent platform that fully automates the process of transforming a user's business idea into a ready-to-deploy web application.

# AppBuilder AI — Documentation & Development Plan

## Core Features
- **Code Generation**: Backend, frontend, and database migrations.
- **Automated Testing**: Generation and execution of tests (RSpec, via `test-generator`).
- **Security Auditing**: Automated security analysis (Brakeman, via `security-auditor`).
- **Self-Correction Cycle**: A fully automated QA → Report → Auto-fixer → Developer → QA loop.
- **Vectorized Codebase Indexing**: Semantic search and navigation through the generated code.
- **LLM Cost Tracking and Limiting**: Monitoring and enforcement of LLM call cost limits.
- **Documentation Generation**: Automated creation of technical documentation (via `doc-generator`).
- **MCP Agent for Plane.so Export**: An agent dedicated to exporting documentation to Plane.so.
- **Advanced Task Management**: Support for priorities, dependencies, and nested subtasks.
- **Automated Issue Creation**: Automated analysis of reports to create actionable fixing tasks.

## API Examples

### Initialize a Project
`POST /projects/init`
```json
{"core_mandate": "A description of the business idea"}
```

### Dispatch a Workflow
`POST /projects/{project_id}/dispatch`
Response: `{ "status": "workflow_started" }`

### Generate Documentation
`POST /projects/{project_id}/docs`
Response: `{ "status": "docs_generated", "path": "..." }`

### Export Documentation to Plane.so
`POST /projects/{project_id}/export_docs`
Body: `{ "plane_api_token": "...", "page_id": null }`

### Run Tests
`POST /projects/{project_id}/run_tests`

### Run a Security Audit
`POST /projects/{project_id}/security_audit`

### Provide Feedback (Live Project Context)
`POST /projects/{project_id}/feedback`
```json
{"feedback": "Add a 'phone' field to the registration form"}
```

## Testing

To run unit tests:
```bash
python -m unittest discover -s backend/tests -p "test_*.py"```

## Best Practices
- All tools are extensible via the `/tools/` directory (e.g., `test_generator`, `auto_fixer`, `doc_generator`, `mcp_plane_exporter`).
- Agents and their roles are described declaratively in `agents.yaml`.
- Leverage iterative cycles and automation to enhance quality.
- The system is designed to support new types of tasks, reports, and business metrics.
- Integration with external platforms is handled via dedicated MCP agents.

---

## Next Steps
1. Enhance `doc-generator` to produce structured documentation from code comments and API definitions.
2. Fully implement the `mcp_plane_exporter` agent for automated documentation export to Plane.so.
3. Integrate and dockerize RSpec and Brakeman to automate testing and auditing workflows.
4. Implement the frontend (React + Tailwind CSS) for visualizing project status and reports.
5. Extend the Live Project Context to handle user feedback and new report types.
6. Achieve comprehensive unit test coverage for all key modules, conduct an architecture review, and optimize the code.
# AppBuilder AI v4.0

An intelligent platform for the automated generation, testing, auditing, and documentation of web applications based on a user's business idea.

## Key Capabilities
- **Iterative Self-Correction Cycle**: The core workflow for ensuring code quality.
- **Extensible Toolset**: Includes tools for test generation, automated code fixing, and documentation creation.
- **Advanced Task Management**: Supports nested tasks, dependencies, priorities, and agent assignment.
- **Detailed Task Statuses**: `pending`, `in_progress`, `awaiting_review`, `completed`, `failed`.
- **Automated Report Analysis**: Automatically analyzes reports from Brakeman and RSpec to create fixing tasks.
- **Vectorized Codebase Indexing**: Enables semantic search across the entire codebase.
- **LLM Cost Management**: Includes cost tracking and enforcement of limits.

## Example Task Structure (`state.json`)
```json
{
  "id": "project-1",
  "status": "in_progress",
  "iteration_count": 0,
  "current_llm_cost": 0.0,
  "tasks": [
    {
      "id": "task-1",
      "agent": "backend-dev",
      "description": "Implement the API for posts",
      "status": "pending",
      "priority": 1,
      "dependencies": [],
      "assigned_to": "backend-dev",
      "artifacts_produced": ["app/models/post.rb", "app/controllers/posts_controller.rb"],
      "subtasks": [
        {"id": "task-1.1", "description": "Create the Post model", "status": "pending"}
      ]
    }
  ],
  "reports": [
    {
      "type": "qa_functional",
      "severity": "medium",
      "content": "Tests are failing for PostsController.",
      "created_at": "2025-08-06T12:00:00Z",
      "related_task": "task-1"
    }
  ]
}
```

## New Tools and Agents
- `/tools/test_generator.py`: Generates RSpec tests.
- `/tools/auto_fixer.py`: Attempts to automatically fix code based on reports.
- `/tools/doc_generator.py`: Generates and updates project documentation.
- **MCP Agent for Plane.so Export**: A dedicated agent for documentation export.

## MCP Agent for Plane.so Export

File: `/tools/mcp_plane_exporter.py`

**Purpose:**
This agent allows for the export of up-to-date project documentation (Live Project Context, specifications, ADRs, reports) to Plane.so via its API.

**Example Usage:**
```python
from praisonai_core.tools.mcp_plane_exporter import export_docs_to_plane

plane_api_token = "<PLANE_SO_API_TOKEN>"
project_id = "example_project_id"
docs = "...generated documentation content..."
url = export_docs_to_plane(project_id, docs, plane_api_token)
print(f"Documentation has been exported: {url}")
```

**Features:**
- Create and update pages in Plane.so.
- Authorize via an API token.
- Return the URL of the page or an error description.

**Recommendation:**
It is recommended to integrate the MCP agent call into the workflow immediately after the `doc-generator` runs to ensure that the knowledge base in Plane.so is always up-to-date.

### New Agents:
- `test-generator`: Generates RSpec tests.
- `auto-fixer`: Automatically attempts to fix code based on reports.
- `doc-generator`: Generates and updates documentation.

## Extensibility
- New tools and agents can be added declaratively via `agents.yaml`.
- The system is designed to support new types of tasks, reports, and business metrics.

## Development Roadmap
- Implement the MCP agent to export the project's Live Project Context (specifications, ADRs, reports) to Plane.so via its API.
  - The agent must support authorization, page creation, and page updates in Plane.so.
  - The integration should be extensible to support other platforms (e.g., Notion, Confluence).
