import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

const pageTitles: Record<string, string> = {
  '/': 'Dashboard',
  '/projects': 'Projects',
  '/crm': 'Customer Relations',
  '/crm/clients': 'Clients',
  '/crm/leads': 'Leads',
  '/crm/deals': 'Deals',
  '/hr': 'Human Resources',
  '/hr/employees': 'Employees',
  '/hr/departments': 'Departments',
  '/hr/leave': 'Leave Requests',
  '/accounting': 'Accounting',
  '/accounting/invoices': 'Invoices',
  '/accounting/expenses': 'Expenses',
  '/equipment': 'Equipment',
  '/production': 'Production',
  '/production/schedules': 'Schedules',
  '/production/locations': 'Locations',
  '/settings': 'Settings',
};

export const MainLayout: React.FC = () => {
  const location = useLocation();
  const title = pageTitles[location.pathname] || 'LitERP';

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="pl-64">
        <Header title={title} />
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
