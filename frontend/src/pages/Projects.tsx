import React from "react";

const mockProjects = [
  { id: "1", name: "AI Workflow Assistant", status: "active" },
  { id: "2", name: "Doc Generator", status: "draft" },
  { id: "3", name: "Plane.so Exporter", status: "archived" },
];

const statusColors: Record<string, string> = {
  active: "bg-green-100 text-green-800",
  draft: "bg-yellow-100 text-yellow-800",
  archived: "bg-gray-200 text-gray-600 dark:bg-neutral-700 dark:text-neutral-300",
};

const Projects: React.FC = () => (
  <div>
    <h1 className="text-2xl font-bold mb-6">Проекты</h1>
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white dark:bg-neutral-800 rounded-lg shadow">
        <thead>
          <tr>
            <th className="px-4 py-2 text-left">Название</th>
            <th className="px-4 py-2 text-left">Статус</th>
            <th className="px-4 py-2 text-left">Действия</th>
          </tr>
        </thead>
        <tbody>
          {mockProjects.map((project) => (
            <tr key={project.id} className="border-t border-gray-100 dark:border-neutral-700">
              <td className="px-4 py-2 font-medium">{project.name}</td>
              <td className="px-4 py-2">
                <span className={`px-2 py-1 rounded text-xs font-semibold ${statusColors[project.status]}`}>{project.status}</span>
              </td>
              <td className="px-4 py-2">
                <a href={`#/project/${project.id}`} className="text-blue-600 hover:underline dark:text-blue-400">Открыть</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export default Projects;
