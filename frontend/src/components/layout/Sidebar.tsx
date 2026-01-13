import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FolderKanban,
  Users,
  Building2,
  FileText,
  Camera,
  Calendar,
  Settings,
  Film,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Projects', href: '/projects', icon: FolderKanban },
  { name: 'CRM', href: '/crm', icon: Users },
  { name: 'HR', href: '/hr', icon: Building2 },
  { name: 'Accounting', href: '/accounting', icon: FileText },
  { name: 'Equipment', href: '/equipment', icon: Camera },
  { name: 'Production', href: '/production', icon: Calendar },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200 z-30">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-gray-200">
        <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
          <Film className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-gray-900">LitERP</h1>
          <p className="text-xs text-gray-500">Video Production</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors
              ${isActive 
                ? 'bg-primary-50 text-primary-700' 
                : 'text-gray-600 hover:bg-gray-100'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};
