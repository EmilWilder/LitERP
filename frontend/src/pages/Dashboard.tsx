import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  FolderKanban,
  CheckCircle2,
  Users,
  TrendingUp,
  FileText,
  AlertCircle,
  Camera,
  Calendar,
  UserCircle,
} from 'lucide-react';
import { Card, Badge, getStatusBadgeVariant } from '../components/ui';
import { dashboardApi } from '../services/api';
import type { DashboardStats } from '../types';

const StatCard: React.FC<{
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  trend?: { value: number; positive: boolean };
  color: string;
}> = ({ title, value, subtitle, icon, color }) => (
  <Card className="flex items-start gap-4">
    <div className={`p-3 rounded-xl ${color}`}>
      {icon}
    </div>
    <div>
      <p className="text-sm text-gray-500">{title}</p>
      <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
      {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
    </div>
  </Card>
);

export const Dashboard: React.FC = () => {
  const { data: stats, isLoading } = useQuery<DashboardStats>({
    queryKey: ['dashboard-stats'],
    queryFn: dashboardApi.getStats,
  });

  const { data: recentActivity } = useQuery({
    queryKey: ['recent-activity'],
    queryFn: dashboardApi.getRecentActivity,
  });

  const { data: myTasks } = useQuery({
    queryKey: ['my-tasks'],
    queryFn: dashboardApi.getMyTasks,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Active Projects"
          value={stats?.projects.active || 0}
          subtitle={`${stats?.projects.completed || 0} completed`}
          icon={<FolderKanban className="w-6 h-6 text-primary-600" />}
          color="bg-primary-50"
        />
        <StatCard
          title="Tasks In Progress"
          value={stats?.tasks.in_progress || 0}
          subtitle={`${stats?.tasks.completed || 0} completed`}
          icon={<CheckCircle2 className="w-6 h-6 text-green-600" />}
          color="bg-green-50"
        />
        <StatCard
          title="Active Clients"
          value={stats?.crm.active_clients || 0}
          subtitle={`${stats?.crm.new_leads || 0} new leads`}
          icon={<Users className="w-6 h-6 text-blue-600" />}
          color="bg-blue-50"
        />
        <StatCard
          title="Pipeline Value"
          value={`$${((stats?.crm.pipeline_value || 0) / 1000).toFixed(0)}k`}
          subtitle={`${stats?.crm.open_deals || 0} open deals`}
          icon={<TrendingUp className="w-6 h-6 text-purple-600" />}
          color="bg-purple-50"
        />
      </div>

      {/* Second Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Pending Invoices"
          value={stats?.finance.pending_invoices || 0}
          subtitle={`$${((stats?.finance.pending_amount || 0) / 1000).toFixed(0)}k outstanding`}
          icon={<FileText className="w-6 h-6 text-orange-600" />}
          color="bg-orange-50"
        />
        <StatCard
          title="Overdue Invoices"
          value={stats?.finance.overdue_invoices || 0}
          icon={<AlertCircle className="w-6 h-6 text-red-600" />}
          color="bg-red-50"
        />
        <StatCard
          title="Equipment Available"
          value={stats?.equipment.available || 0}
          subtitle={`${stats?.equipment.in_use || 0} in use`}
          icon={<Camera className="w-6 h-6 text-teal-600" />}
          color="bg-teal-50"
        />
        <StatCard
          title="Upcoming Shoots"
          value={stats?.production.upcoming_shoots || 0}
          icon={<Calendar className="w-6 h-6 text-indigo-600" />}
          color="bg-indigo-50"
        />
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* My Tasks */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">My Tasks</h3>
            <Badge variant="info">{myTasks?.length || 0}</Badge>
          </div>
          <div className="space-y-3">
            {myTasks?.length === 0 ? (
              <p className="text-gray-500 text-sm">No tasks assigned</p>
            ) : (
              myTasks?.slice(0, 5).map((task: any) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono text-gray-500">{task.task_key}</span>
                    <span className="text-sm font-medium text-gray-900">{task.title}</span>
                  </div>
                  <Badge variant={getStatusBadgeVariant(task.status)}>
                    {task.status.replace('_', ' ')}
                  </Badge>
                </div>
              ))
            )}
          </div>
        </Card>

        {/* Recent Activity */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recent Projects</h3>
          </div>
          <div className="space-y-3">
            {recentActivity?.recent_projects?.length === 0 ? (
              <p className="text-gray-500 text-sm">No recent projects</p>
            ) : (
              recentActivity?.recent_projects?.map((project: any) => (
                <div
                  key={project.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                      <FolderKanban className="w-4 h-4 text-primary-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{project.name}</p>
                      <p className="text-xs text-gray-500">{project.code}</p>
                    </div>
                  </div>
                  <Badge variant={getStatusBadgeVariant(project.status)}>
                    {project.status.replace('_', ' ')}
                  </Badge>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>

      {/* HR Summary */}
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Team Overview</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
              <UserCircle className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats?.hr.total_employees || 0}</p>
              <p className="text-sm text-gray-500">Total Employees</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-yellow-50 rounded-xl flex items-center justify-center">
              <Calendar className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats?.hr.pending_leave_requests || 0}</p>
              <p className="text-sm text-gray-500">Pending Leave Requests</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center">
              <Camera className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats?.production.upcoming_shoots || 0}</p>
              <p className="text-sm text-gray-500">Shoots This Week</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
