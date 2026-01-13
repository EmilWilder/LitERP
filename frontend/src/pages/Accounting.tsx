import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { NavLink, Routes, Route } from 'react-router-dom';
import { Plus, FileText, Receipt, DollarSign } from 'lucide-react';
import { Card, Button, Input, Badge, getStatusBadgeVariant, Modal, Select, Table } from '../components/ui';
import { accountingApi, crmApi, projectsApi } from '../services/api';
import { Invoice, Expense, Client, Project } from '../types';
import { format } from 'date-fns';

const AccountingNav: React.FC = () => (
  <div className="flex gap-1 mb-6 bg-gray-100 p-1 rounded-lg w-fit">
    {[
      { to: '/accounting', label: 'Invoices', icon: FileText, end: true },
      { to: '/accounting/expenses', label: 'Expenses', icon: Receipt },
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

// Invoices Page
const InvoicesPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: invoices, isLoading } = useQuery<Invoice[]>({
    queryKey: ['invoices'],
    queryFn: () => accountingApi.listInvoices(),
  });

  const { data: clients } = useQuery<Client[]>({
    queryKey: ['clients'],
    queryFn: () => crmApi.listClients(),
  });

  const { data: projects } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: () => projectsApi.list(),
  });

  const createMutation = useMutation({
    mutationFn: accountingApi.createInvoice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      invoice_number: formData.get('invoice_number'),
      client_id: parseInt(formData.get('client_id') as string),
      project_id: parseInt(formData.get('project_id') as string) || null,
      issue_date: formData.get('issue_date'),
      due_date: formData.get('due_date'),
      tax_rate: parseFloat(formData.get('tax_rate') as string) || 0,
      items: [{
        description: formData.get('item_description') as string,
        quantity: 1,
        unit_price: parseFloat(formData.get('item_amount') as string) || 0,
      }],
    });
  };

  const columns = [
    { key: 'invoice_number', header: 'Invoice #', render: (i: Invoice) => <span className="font-mono">{i.invoice_number}</span> },
    { key: 'client_id', header: 'Client', render: (i: Invoice) => clients?.find(c => c.id === i.client_id)?.name || '-' },
    { key: 'project_id', header: 'Project', render: (i: Invoice) => projects?.find(p => p.id === i.project_id)?.name || '-' },
    { key: 'issue_date', header: 'Issue Date', render: (i: Invoice) => format(new Date(i.issue_date), 'MMM d, yyyy') },
    { key: 'due_date', header: 'Due Date', render: (i: Invoice) => format(new Date(i.due_date), 'MMM d, yyyy') },
    { key: 'total_amount', header: 'Total', render: (i: Invoice) => <span className="font-medium">${i.total_amount.toLocaleString()}</span> },
    { key: 'balance_due', header: 'Balance', render: (i: Invoice) => <span className={i.balance_due > 0 ? 'text-red-600' : 'text-green-600'}>${i.balance_due.toLocaleString()}</span> },
    { key: 'status', header: 'Status', render: (i: Invoice) => (
      <Badge variant={getStatusBadgeVariant(i.status)}>{i.status}</Badge>
    )},
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Invoices</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Create Invoice
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={invoices || []} keyExtractor={(i) => i.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Create New Invoice" size="lg">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Invoice Number" name="invoice_number" required placeholder="e.g., INV-2026-001" />
            <Select
              label="Client"
              name="client_id"
              options={clients?.map(c => ({ value: c.id.toString(), label: c.name })) || []}
              placeholder="Select client"
              required
            />
          </div>
          <Select
            label="Project (Optional)"
            name="project_id"
            options={projects?.map(p => ({ value: p.id.toString(), label: `${p.code} - ${p.name}` })) || []}
            placeholder="Select project"
          />
          <div className="grid grid-cols-3 gap-4">
            <Input label="Issue Date" name="issue_date" type="date" required />
            <Input label="Due Date" name="due_date" type="date" required />
            <Input label="Tax Rate (%)" name="tax_rate" type="number" placeholder="0" />
          </div>
          
          <div className="border-t pt-4">
            <h4 className="font-medium text-gray-900 mb-3">Line Item</h4>
            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <Input label="Description" name="item_description" required placeholder="e.g., Video Production Services" />
              </div>
              <Input label="Amount" name="item_amount" type="number" required placeholder="0" />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Create Invoice</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

// Expenses Page
const ExpensesPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: expenses, isLoading } = useQuery<Expense[]>({
    queryKey: ['expenses'],
    queryFn: () => accountingApi.listExpenses(),
  });

  const { data: projects } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: () => projectsApi.list(),
  });

  const createMutation = useMutation({
    mutationFn: accountingApi.createExpense,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      setShowModal(false);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => accountingApi.updateExpense(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      category: formData.get('category'),
      description: formData.get('description'),
      amount: parseFloat(formData.get('amount') as string),
      expense_date: formData.get('expense_date'),
      project_id: parseInt(formData.get('project_id') as string) || null,
      vendor_name: formData.get('vendor_name'),
      is_reimbursable: formData.get('is_reimbursable') === 'on',
    });
  };

  const columns = [
    { key: 'expense_number', header: 'Expense #', render: (e: Expense) => <span className="font-mono text-xs">{e.expense_number}</span> },
    { key: 'category', header: 'Category', render: (e: Expense) => <Badge>{e.category.replace('_', ' ')}</Badge> },
    { key: 'description', header: 'Description', render: (e: Expense) => <span className="max-w-xs truncate">{e.description}</span> },
    { key: 'project_id', header: 'Project', render: (e: Expense) => projects?.find(p => p.id === e.project_id)?.code || '-' },
    { key: 'amount', header: 'Amount', render: (e: Expense) => <span className="font-medium">${e.amount.toLocaleString()}</span> },
    { key: 'expense_date', header: 'Date', render: (e: Expense) => format(new Date(e.expense_date), 'MMM d, yyyy') },
    { key: 'status', header: 'Status', render: (e: Expense) => (
      <Badge variant={getStatusBadgeVariant(e.status)}>{e.status}</Badge>
    )},
    { key: 'actions', header: 'Actions', render: (e: Expense) => e.status === 'pending' && (
      <div className="flex gap-2">
        <Button size="sm" variant="ghost" onClick={() => updateMutation.mutate({ id: e.id, data: { status: 'approved' } })}>
          Approve
        </Button>
      </div>
    )},
  ];

  const categoryOptions = [
    { value: 'equipment_rental', label: 'Equipment Rental' },
    { value: 'talent', label: 'Talent' },
    { value: 'crew', label: 'Crew' },
    { value: 'location', label: 'Location' },
    { value: 'catering', label: 'Catering' },
    { value: 'transportation', label: 'Transportation' },
    { value: 'accommodation', label: 'Accommodation' },
    { value: 'post_production', label: 'Post Production' },
    { value: 'music_licensing', label: 'Music Licensing' },
    { value: 'props', label: 'Props' },
    { value: 'wardrobe', label: 'Wardrobe' },
    { value: 'insurance', label: 'Insurance' },
    { value: 'permits', label: 'Permits' },
    { value: 'software', label: 'Software' },
    { value: 'other', label: 'Other' },
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Expenses</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Expense
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={expenses || []} keyExtractor={(e) => e.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Expense">
        <form onSubmit={handleCreate} className="space-y-4">
          <Select
            label="Category"
            name="category"
            options={categoryOptions}
            placeholder="Select category"
            required
          />
          <Input label="Description" name="description" required placeholder="e.g., Camera rental for Day 1" />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Amount" name="amount" type="number" step="0.01" required placeholder="0.00" />
            <Input label="Date" name="expense_date" type="date" required />
          </div>
          <Select
            label="Project (Optional)"
            name="project_id"
            options={projects?.map(p => ({ value: p.id.toString(), label: `${p.code} - ${p.name}` })) || []}
            placeholder="Select project"
          />
          <Input label="Vendor" name="vendor_name" placeholder="e.g., ABC Rentals" />
          <div className="flex items-center gap-2">
            <input type="checkbox" name="is_reimbursable" id="is_reimbursable" className="rounded border-gray-300" />
            <label htmlFor="is_reimbursable" className="text-sm text-gray-700">Reimbursable expense</label>
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Expense</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

export const Accounting: React.FC = () => {
  return (
    <div>
      <AccountingNav />
      <Routes>
        <Route index element={<InvoicesPage />} />
        <Route path="expenses" element={<ExpensesPage />} />
      </Routes>
    </div>
  );
};
