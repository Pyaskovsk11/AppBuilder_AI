import React from "react";
import { useParams, Link } from "react-router-dom";

const mockProjects = [
  { id: "1", name: "AI Workflow Assistant", status: "active", description: "Автоматизация рабочих процессов с помощью ИИ-агентов." },
  { id: "2", name: "Doc Generator", status: "draft", description: "Генерация документации на основе кода и спецификаций." },
  { id: "3", name: "Plane.so Exporter", status: "archived", description: "Экспорт задач и спецификаций в Plane.so." },
];

const ProjectDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const project = mockProjects.find((p) => p.id === id);

  if (!project) {
    return <div className="text-red-600">Проект не найден</div>;
  }

  const [tab, setTab] = React.useState('tasks');
  const tabs = [
    { key: 'tasks', label: 'Задачи' },
    { key: 'tests', label: 'Тесты' },
    { key: 'docs', label: 'Документация' },
    { key: 'history', label: 'История' },
    { key: 'settings', label: 'Настройки' },
  ];

  // Мок-данные задач

  type TaskStatus = 'done' | 'in_progress' | 'todo';
  interface Task {
    id: string;
    title: string;
    status: TaskStatus;
    assignee: string;
    due: string;
  }
  const mockTasks: Task[] = [
    { id: 't1', title: 'Реализовать API генерации документации', status: 'done', assignee: 'Иван', due: '2025-08-10' },
    { id: 't2', title: 'Интеграция Plane.so экспорта', status: 'in_progress', assignee: 'Мария', due: '2025-08-12' },
    { id: 't3', title: 'Добавить semantic code search', status: 'todo', assignee: 'Алексей', due: '2025-08-15' },
  ];
  const statusMap: Record<TaskStatus, { label: string; color: string }> = {
    done: { label: 'Готово', color: 'bg-green-100 text-green-800' },
    in_progress: { label: 'В работе', color: 'bg-yellow-100 text-yellow-800' },
    todo: { label: 'План' , color: 'bg-gray-100 text-gray-700 dark:bg-neutral-700 dark:text-neutral-200' },
  };

  return (
    <div>
      <Link to="/projects" className="text-blue-600 hover:underline dark:text-blue-400 mb-4 inline-block">← Назад к проектам</Link>
      <h1 className="text-2xl font-bold mb-2">{project.name}</h1>
      <span className="inline-block mb-4 px-2 py-1 rounded text-xs font-semibold bg-gray-200 text-gray-600 dark:bg-neutral-700 dark:text-neutral-300">{project.status}</span>
      <div className="bg-white dark:bg-neutral-800 rounded-lg shadow p-6 mb-6">
        <p className="text-gray-700 dark:text-gray-200 mb-2">{project.description}</p>
        <div className="border-b border-gray-200 dark:border-neutral-700 mb-4">
          <nav className="flex space-x-4">
            {tabs.map((t) => (
              <button
                key={t.key}
                onClick={() => setTab(t.key)}
                className={`px-3 py-1 text-sm font-medium rounded-t transition-colors
                  ${tab === t.key ? 'bg-gray-100 dark:bg-neutral-900 text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400' : 'text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'}`}
                style={{ borderBottom: tab === t.key ? undefined : '2px solid transparent' }}
              >
                {t.label}
              </button>
            ))}
          </nav>
        </div>
        <div>
          {tab === 'tasks' && (
            <div>
              <h2 className="text-lg font-semibold mb-3">Список задач</h2>
              <table className="min-w-full bg-white dark:bg-neutral-800 rounded shadow">
                <thead>
                  <tr>
                    <th className="px-3 py-2 text-left">Название</th>
                    <th className="px-3 py-2 text-left">Статус</th>
                    <th className="px-3 py-2 text-left">Исполнитель</th>
                    <th className="px-3 py-2 text-left">Срок</th>
                  </tr>
                </thead>
                <tbody>
                  {mockTasks.map((task) => (
                    <tr key={task.id} className="border-t border-gray-100 dark:border-neutral-700">
                      <td className="px-3 py-2">{task.title}</td>
                      <td className="px-3 py-2">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${statusMap[task.status].color}`}>{statusMap[task.status].label}</span>
                      </td>
                      <td className="px-3 py-2">{task.assignee}</td>
                      <td className="px-3 py-2">{task.due}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {tab === 'tests' && <div className="text-gray-700 dark:text-gray-200">(Здесь будет информация о тестах и CI/CD)</div>}
          {tab === 'docs' && <div className="text-gray-700 dark:text-gray-200">(Здесь будет документация проекта)</div>}
          {tab === 'history' && <div className="text-gray-700 dark:text-gray-200">(Здесь будет история изменений и событий)</div>}
          {tab === 'settings' && <div className="text-gray-700 dark:text-gray-200">(Здесь будут настройки проекта)</div>}
        </div>
      </div>
    </div>
  );
};

export default ProjectDetails;
