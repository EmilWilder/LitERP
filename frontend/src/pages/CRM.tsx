import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { NavLink, Routes, Route } from 'react-router-dom';
import { Plus, Target, HandshakeIcon, Building2, Phone, Mail } from 'lucide-react';
import { Card, Button, Input, Badge, getStatusBadgeVariant, Modal, Select, Table } from '../components/ui';
import { crmApi } from '../services/api';
import type { Client, Lead, Deal } from '../types';
import { format } from 'date-fns';

const CRMNav: React.FC = () => (
  <div className="flex gap-1 mb-6 bg-gray-100 p-1 rounded-lg w-fit">
    {[
      { to: '/crm', label: 'Clients', icon: Building2, end: true },
      { to: '/crm/leads', label: 'Leads', icon: Target },
      { to: '/crm/deals', label: 'Deals', icon: HandshakeIcon },
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

// Clients Page
const ClientsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: clients, isLoading } = useQuery<Client[]>({
    queryKey: ['clients'],
    queryFn: () => crmApi.listClients(),
  });

  const createMutation = useMutation({
    mutationFn: crmApi.createClient,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clients'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      name: formData.get('name'),
      code: formData.get('code'),
      client_type: formData.get('client_type'),
      email: formData.get('email'),
      phone: formData.get('phone'),
      industry: formData.get('industry'),
    });
  };

  const columns = [
    { key: 'code', header: 'Code', render: (c: Client) => <span className="font-mono text-xs">{c.code}</span> },
    { key: 'name', header: 'Name', render: (c: Client) => <span className="font-medium">{c.name}</span> },
    { key: 'client_type', header: 'Type', render: (c: Client) => <Badge>{c.client_type.replace('_', ' ')}</Badge> },
    { key: 'email', header: 'Contact', render: (c: Client) => (
      <div className="flex flex-col gap-1">
        {c.email && <span className="text-xs flex items-center gap-1"><Mail className="w-3 h-3" />{c.email}</span>}
        {c.phone && <span className="text-xs flex items-center gap-1"><Phone className="w-3 h-3" />{c.phone}</span>}
      </div>
    )},
    { key: 'industry', header: 'Industry' },
    { key: 'is_active', header: 'Status', render: (c: Client) => (
      <Badge variant={c.is_active ? 'success' : 'default'}>{c.is_active ? 'Active' : 'Inactive'}</Badge>
    )},
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Clients</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Client
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={clients || []} keyExtractor={(c) => c.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Client">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Client Name" name="name" required />
            <Input label="Code" name="code" required placeholder="e.g., ACME" />
          </div>
          <Select
            label="Client Type"
            name="client_type"
            options={[
              { value: 'agency', label: 'Agency' },
              { value: 'brand', label: 'Brand' },
              { value: 'production_company', label: 'Production Company' },
              { value: 'broadcaster', label: 'Broadcaster' },
              { value: 'streaming_platform', label: 'Streaming Platform' },
              { value: 'individual', label: 'Individual' },
            ]}
          />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Email" name="email" type="email" />
            <Input label="Phone" name="phone" />
          </div>
          <Input label="Industry" name="industry" />
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Client</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

// Leads Page
const LeadsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: leads, isLoading } = useQuery<Lead[]>({
    queryKey: ['leads'],
    queryFn: () => crmApi.listLeads(),
  });

  const createMutation = useMutation({
    mutationFn: crmApi.createLead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leads'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      title: formData.get('title'),
      contact_name: formData.get('contact_name'),
      contact_email: formData.get('contact_email'),
      company_name: formData.get('company_name'),
      source: formData.get('source'),
      estimated_value: parseFloat(formData.get('estimated_value') as string) || 0,
    });
  };

  const columns = [
    { key: 'title', header: 'Title', render: (l: Lead) => <span className="font-medium">{l.title}</span> },
    { key: 'company_name', header: 'Company' },
    { key: 'contact_name', header: 'Contact' },
    { key: 'source', header: 'Source', render: (l: Lead) => <Badge>{l.source.replace('_', ' ')}</Badge> },
    { key: 'estimated_value', header: 'Value', render: (l: Lead) => l.estimated_value ? `$${l.estimated_value.toLocaleString()}` : '-' },
    { key: 'status', header: 'Status', render: (l: Lead) => (
      <Badge variant={getStatusBadgeVariant(l.status)}>{l.status.replace('_', ' ')}</Badge>
    )},
    { key: 'created_at', header: 'Created', render: (l: Lead) => format(new Date(l.created_at), 'MMM d, yyyy') },
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Leads</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Lead
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={leads || []} keyExtractor={(l) => l.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Lead">
        <form onSubmit={handleCreate} className="space-y-4">
          <Input label="Lead Title" name="title" required placeholder="e.g., Corporate Video Project" />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Contact Name" name="contact_name" />
            <Input label="Contact Email" name="contact_email" type="email" />
          </div>
          <Input label="Company Name" name="company_name" />
          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Source"
              name="source"
              options={[
                { value: 'website', label: 'Website' },
                { value: 'referral', label: 'Referral' },
                { value: 'social_media', label: 'Social Media' },
                { value: 'cold_call', label: 'Cold Call' },
                { value: 'trade_show', label: 'Trade Show' },
              ]}
            />
            <Input label="Estimated Value" name="estimated_value" type="number" placeholder="0" />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Lead</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

// Deals Page
const DealsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: deals, isLoading } = useQuery<Deal[]>({
    queryKey: ['deals'],
    queryFn: () => crmApi.listDeals(),
  });

  const { data: clients } = useQuery<Client[]>({
    queryKey: ['clients'],
    queryFn: () => crmApi.listClients(),
  });

  const createMutation = useMutation({
    mutationFn: crmApi.createDeal,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      name: formData.get('name'),
      client_id: parseInt(formData.get('client_id') as string),
      amount: parseFloat(formData.get('amount') as string) || 0,
      probability: parseInt(formData.get('probability') as string) || 50,
    });
  };

  const columns = [
    { key: 'name', header: 'Deal', render: (d: Deal) => <span className="font-medium">{d.name}</span> },
    { key: 'client_id', header: 'Client', render: (d: Deal) => clients?.find(c => c.id === d.client_id)?.name || '-' },
    { key: 'stage', header: 'Stage', render: (d: Deal) => (
      <Badge variant={getStatusBadgeVariant(d.stage)}>{d.stage.replace('_', ' ')}</Badge>
    )},
    { key: 'amount', header: 'Amount', render: (d: Deal) => `$${d.amount.toLocaleString()}` },
    { key: 'probability', header: 'Probability', render: (d: Deal) => `${d.probability}%` },
    { key: 'expected_revenue', header: 'Expected', render: (d: Deal) => `$${d.expected_revenue.toLocaleString()}` },
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Deals</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Deal
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={deals || []} keyExtractor={(d) => d.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Deal">
        <form onSubmit={handleCreate} className="space-y-4">
          <Input label="Deal Name" name="name" required />
          <Select
            label="Client"
            name="client_id"
            options={clients?.map(c => ({ value: c.id.toString(), label: c.name })) || []}
            placeholder="Select client"
            required
          />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Amount" name="amount" type="number" placeholder="0" />
            <Input label="Probability (%)" name="probability" type="number" placeholder="50" />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Deal</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

export const CRM: React.FC = () => {
  return (
    <div>
      <CRMNav />
      <Routes>
        <Route index element={<ClientsPage />} />
        <Route path="leads" element={<LeadsPage />} />
        <Route path="deals" element={<DealsPage />} />
      </Routes>
    </div>
  );
};
