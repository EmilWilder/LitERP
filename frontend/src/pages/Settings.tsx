import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, User, Shield, Mail } from 'lucide-react';
import { Card, Button, Input, Badge, Modal, Select, Table } from '../components/ui';
import { usersApi } from '../services/api';
import type { User as UserType } from '../types';

const roleOptions = [
  { value: 'admin', label: 'Admin' },
  { value: 'manager', label: 'Manager' },
  { value: 'producer', label: 'Producer' },
  { value: 'editor', label: 'Editor' },
  { value: 'cameraman', label: 'Cameraman' },
  { value: 'accountant', label: 'Accountant' },
  { value: 'hr', label: 'HR' },
  { value: 'sales', label: 'Sales' },
  { value: 'employee', label: 'Employee' },
];

export const Settings: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: users, isLoading } = useQuery<UserType[]>({
    queryKey: ['users'],
    queryFn: () => usersApi.list(),
  });

  const createMutation = useMutation({
    mutationFn: usersApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      username: formData.get('username'),
      email: formData.get('email'),
      password: formData.get('password'),
      full_name: formData.get('full_name'),
      role: formData.get('role'),
      phone: formData.get('phone'),
    });
  };

  const columns = [
    { key: 'username', header: 'Username', render: (u: UserType) => (
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
          <User className="w-4 h-4 text-primary-600" />
        </div>
        <span className="font-medium">{u.username}</span>
      </div>
    )},
    { key: 'full_name', header: 'Full Name', render: (u: UserType) => u.full_name || '-' },
    { key: 'email', header: 'Email', render: (u: UserType) => (
      <span className="flex items-center gap-1 text-gray-600">
        <Mail className="w-3 h-3" />
        {u.email}
      </span>
    )},
    { key: 'role', header: 'Role', render: (u: UserType) => (
      <Badge variant={u.role === 'admin' ? 'danger' : u.role === 'manager' ? 'purple' : 'default'}>
        {u.role}
      </Badge>
    )},
    { key: 'is_active', header: 'Status', render: (u: UserType) => (
      <Badge variant={u.is_active ? 'success' : 'default'}>
        {u.is_active ? 'Active' : 'Inactive'}
      </Badge>
    )},
    { key: 'is_superuser', header: 'Admin', render: (u: UserType) => u.is_superuser && (
      <Shield className="w-4 h-4 text-red-500" />
    )},
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold">User Management</h2>
          <p className="text-sm text-gray-500">Manage user accounts and permissions</p>
        </div>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add User
        </Button>
      </div>

      <Card padding="none">
        <Table
          columns={columns}
          data={users || []}
          keyExtractor={(u) => u.id}
          isLoading={isLoading}
        />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New User">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Username" name="username" required placeholder="johndoe" />
            <Input label="Email" name="email" type="email" required placeholder="john@example.com" />
          </div>
          <Input label="Full Name" name="full_name" placeholder="John Doe" />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Password" name="password" type="password" required placeholder="••••••••" />
            <Input label="Phone" name="phone" placeholder="+1 234 567 8900" />
          </div>
          <Select
            label="Role"
            name="role"
            options={roleOptions}
            placeholder="Select role"
            required
          />
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Create User</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
