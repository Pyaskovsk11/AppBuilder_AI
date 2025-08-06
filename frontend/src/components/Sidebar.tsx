import React from "react";
import { Link, useLocation } from "react-router-dom";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/projects", label: "Проекты" },
  { to: "#", label: "Документация" },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  return (
    <aside className="w-64 bg-gray-100 dark:bg-neutral-800 border-r border-gray-200 dark:border-neutral-800 p-4 hidden md:block">
      <nav>
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.to}>
              <Link
                to={item.to}
                className={`block px-2 py-1 rounded hover:bg-gray-200 dark:hover:bg-neutral-700 text-gray-900 dark:text-white ${location.pathname === item.to ? 'font-bold bg-gray-200 dark:bg-neutral-700' : ''}`}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
