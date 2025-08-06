import React from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => (
  <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-neutral-900">
    <Header />
    <div className="flex flex-1">
      <Sidebar />
      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  </div>
);

export default Layout;
