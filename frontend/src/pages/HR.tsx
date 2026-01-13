import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { NavLink, Routes, Route } from 'react-router-dom';
import { Plus, Users, Building2, Calendar } from 'lucide-react';
import { Card, Button, Input, Badge, getStatusBadgeVariant, Modal, Select, Table } from '../components/ui';
import { hrApi, usersApi } from '../services/api';
import type { Employee, Department } from '../types';
import { format } from 'date-fns';

const HRNav: React.FC = () => (
  <div className="flex gap-1 mb-6 bg-gray-100 p-1 rounded-lg w-fit">
    {[
      { to: '/hr', label: 'Employees', icon: Users, end: true },
      { to: '/hr/departments', label: 'Departments', icon: Building2 },
      { to: '/hr/leave', label: 'Leave Requests', icon: Calendar },
    ].map(({ to, label, icon: Icon, end }) => (
      <NavLink
        key={to}
        to={to}
        end={end}
        className={({ isActive }) =>
          `flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            isActive ? 'bg-white shadow text-primary-700' : 'text-gray-600 hover:text-gray-900'
          }`
        }
      >
        <Icon className="w-4 h-4" />
        {label}
      </NavLink>
    ))}
  </div>
);

// Employees Page
const EmployeesPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: employees, isLoading } = useQuery<Employee[]>({
    queryKey: ['employees'],
    queryFn: () => hrApi.listEmployees(),
  });

  const { data: departments } = useQuery<Department[]>({
    queryKey: ['departments'],
    queryFn: () => hrApi.listDepartments(),
  });

  const { data: users } = useQuery({
    queryKey: ['users'],
    queryFn: () => usersApi.list(),
  });

  const createMutation = useMutation({
    mutationFn: hrApi.createEmployee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      user_id: parseInt(formData.get('user_id') as string),
      employee_code: formData.get('employee_code'),
      job_title: formData.get('job_title'),
      department_id: parseInt(formData.get('department_id') as string) || null,
      employment_type: formData.get('employment_type'),
      hire_date: formData.get('hire_date'),
      salary: parseFloat(formData.get('salary') as string) || 0,
    });
  };

  const columns = [
    { key: 'employee_code', header: 'ID', render: (e: Employee) => <span className="font-mono text-xs">{e.employee_code}</span> },
    { key: 'job_title', header: 'Position', render: (e: Employee) => <span className="font-medium">{e.job_title}</span> },
    { key: 'employment_type', header: 'Type', render: (e: Employee) => <Badge>{e.employment_type.replace('_', ' ')}</Badge> },
    { key: 'department_id', header: 'Department', render: (e: Employee) => departments?.find(d => d.id === e.department_id)?.name || '-' },
    { key: 'hire_date', header: 'Hire Date', render: (e: Employee) => format(new Date(e.hire_date), 'MMM d, yyyy') },
    { key: 'is_active', header: 'Status', render: (e: Employee) => (
      <Badge variant={e.is_active ? 'success' : 'default'}>{e.is_active ? 'Active' : 'Inactive'}</Badge>
    )},
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Employees</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Employee
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={employees || []} keyExtractor={(e) => e.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Employee">
        <form onSubmit={handleCreate} className="space-y-4">
          <Select
            label="User Account"
            name="user_id"
            options={users?.map((u: any) => ({ value: u.id.toString(), label: u.full_name || u.username })) || []}
            placeholder="Select user"
            required
          />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Employee Code" name="employee_code" required placeholder="e.g., EMP-001" />
            <Input label="Job Title" name="job_title" required placeholder="e.g., Video Editor" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Department"
              name="department_id"
              options={departments?.map(d => ({ value: d.id.toString(), label: d.name })) || []}
              placeholder="Select department"
            />
            <Select
              label="Employment Type"
              name="employment_type"
              options={[
                { value: 'full_time', label: 'Full Time' },
                { value: 'part_time', label: 'Part Time' },
                { value: 'contract', label: 'Contract' },
                { value: 'freelance', label: 'Freelance' },
                { value: 'intern', label: 'Intern' },
              ]}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Hire Date" name="hire_date" type="date" required />
            <Input label="Salary" name="salary" type="number" placeholder="0" />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Employee</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

// Departments Page
const DepartmentsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: departments, isLoading } = useQuery<Department[]>({
    queryKey: ['departments'],
    queryFn: () => hrApi.listDepartments(),
  });

  const createMutation = useMutation({
    mutationFn: hrApi.createDepartment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departments'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      name: formData.get('name'),
      code: formData.get('code'),
      description: formData.get('description'),
      budget: parseFloat(formData.get('budget') as string) || 0,
    });
  };

  const columns = [
    { key: 'code', header: 'Code', render: (d: Department) => <span className="font-mono text-xs">{d.code}</span> },
    { key: 'name', header: 'Name', render: (d: Department) => <span className="font-medium">{d.name}</span> },
    { key: 'description', header: 'Description', render: (d: Department) => d.description || '-' },
    { key: 'budget', header: 'Budget', render: (d: Department) => `$${d.budget.toLocaleString()}` },
    { key: 'is_active', header: 'Status', render: (d: Department) => (
      <Badge variant={d.is_active ? 'success' : 'default'}>{d.is_active ? 'Active' : 'Inactive'}</Badge>
    )},
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Departments</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Department
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={departments || []} keyExtractor={(d) => d.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Department">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Department Name" name="name" required placeholder="e.g., Post Production" />
            <Input label="Code" name="code" required placeholder="e.g., POST" />
          </div>
          <Input label="Budget" name="budget" type="number" placeholder="0" />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              name="description"
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
            />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Department</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

// Leave Requests Page
const LeaveRequestsPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: leaveRequests, isLoading } = useQuery({
    queryKey: ['leave-requests'],
    queryFn: () => hrApi.listLeaveRequests(),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => hrApi.updateLeaveRequest(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leave-requests'] });
    },
  });

  const columns = [
    { key: 'employee_id', header: 'Employee', render: (l: any) => `Employee #${l.employee_id}` },
    { key: 'leave_type', header: 'Type', render: (l: any) => <Badge>{l.leave_type}</Badge> },
    { key: 'start_date', header: 'Start', render: (l: any) => format(new Date(l.start_date), 'MMM d, yyyy') },
    { key: 'end_date', header: 'End', render: (l: any) => format(new Date(l.end_date), 'MMM d, yyyy') },
    { key: 'total_days', header: 'Days' },
    { key: 'status', header: 'Status', render: (l: any) => (
      <Badge variant={getStatusBadgeVariant(l.status)}>{l.status}</Badge>
    )},
    { key: 'actions', header: 'Actions', render: (l: any) => l.status === 'pending' && (
      <div className="flex gap-2">
        <Button size="sm" variant="ghost" onClick={() => updateMutation.mutate({ id: l.id, data: { status: 'approved' } })}>
          Approve
        </Button>
        <Button size="sm" variant="ghost" className="text-red-600" onClick={() => updateMutation.mutate({ id: l.id, data: { status: 'rejected' } })}>
          Reject
        </Button>
      </div>
    )},
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Leave Requests</h2>
      </div>
      <Card padding="none">
        <Table columns={columns} data={leaveRequests || []} keyExtractor={(l) => l.id} isLoading={isLoading} />
      </Card>
    </>
  );
};

export const HR: React.FC = () => {
  return (
    <div>
      <HRNav />
      <Routes>
        <Route index element={<EmployeesPage />} />
        <Route path="departments" element={<DepartmentsPage />} />
        <Route path="leave" element={<LeaveRequestsPage />} />
      </Routes>
    </div>
  );
};
