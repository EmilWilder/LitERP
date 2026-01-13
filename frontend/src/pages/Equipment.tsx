import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Camera, Search, Calendar, AlertCircle } from 'lucide-react';
import { Card, Button, Input, Badge, getStatusBadgeVariant, Modal, Select, Table } from '../components/ui';
import { equipmentApi } from '../services/api';
import { Equipment as EquipmentType } from '../types';
import { format } from 'date-fns';

const categoryOptions = [
  { value: 'camera', label: 'Camera' },
  { value: 'lens', label: 'Lens' },
  { value: 'lighting', label: 'Lighting' },
  { value: 'audio', label: 'Audio' },
  { value: 'grip', label: 'Grip' },
  { value: 'support', label: 'Support (Tripods, Gimbals)' },
  { value: 'drone', label: 'Drone' },
  { value: 'monitor', label: 'Monitor' },
  { value: 'storage', label: 'Storage' },
  { value: 'computer', label: 'Computer' },
  { value: 'vehicle', label: 'Vehicle' },
  { value: 'other', label: 'Other' },
];

export const Equipment: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const queryClient = useQueryClient();

  const { data: equipment, isLoading } = useQuery<EquipmentType[]>({
    queryKey: ['equipment'],
    queryFn: () => equipmentApi.list(),
  });

  const createMutation = useMutation({
    mutationFn: equipmentApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['equipment'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      name: formData.get('name'),
      code: formData.get('code'),
      category: formData.get('category'),
      brand: formData.get('brand'),
      model: formData.get('model'),
      serial_number: formData.get('serial_number'),
      purchase_date: formData.get('purchase_date') || null,
      purchase_price: parseFloat(formData.get('purchase_price') as string) || null,
      daily_rate: parseFloat(formData.get('daily_rate') as string) || null,
      storage_location: formData.get('storage_location'),
    });
  };

  const filteredEquipment = equipment?.filter(eq => {
    const matchesSearch = eq.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      eq.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (eq.brand && eq.brand.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = !categoryFilter || eq.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  const columns = [
    { key: 'code', header: 'Asset Code', render: (e: EquipmentType) => <span className="font-mono text-xs">{e.code}</span> },
    { key: 'name', header: 'Name', render: (e: EquipmentType) => (
      <div>
        <span className="font-medium">{e.name}</span>
        {e.brand && e.model && <span className="text-gray-500 text-xs block">{e.brand} {e.model}</span>}
      </div>
    )},
    { key: 'category', header: 'Category', render: (e: EquipmentType) => <Badge>{e.category}</Badge> },
    { key: 'status', header: 'Status', render: (e: EquipmentType) => (
      <Badge variant={getStatusBadgeVariant(e.status)}>{e.status.replace('_', ' ')}</Badge>
    )},
    { key: 'storage_location', header: 'Location', render: (e: EquipmentType) => e.storage_location || '-' },
    { key: 'daily_rate', header: 'Daily Rate', render: (e: EquipmentType) => e.daily_rate ? `$${e.daily_rate}` : '-' },
    { key: 'next_maintenance_date', header: 'Next Maintenance', render: (e: EquipmentType) => {
      if (!e.next_maintenance_date) return '-';
      const date = new Date(e.next_maintenance_date);
      const isOverdue = date < new Date();
      return (
        <span className={isOverdue ? 'text-red-600 flex items-center gap-1' : ''}>
          {isOverdue && <AlertCircle className="w-3 h-3" />}
          {format(date, 'MMM d, yyyy')}
        </span>
      );
    }},
  ];

  // Summary stats
  const stats = {
    total: equipment?.length || 0,
    available: equipment?.filter(e => e.status === 'available').length || 0,
    inUse: equipment?.filter(e => e.status === 'in_use').length || 0,
    maintenance: equipment?.filter(e => e.status === 'maintenance').length || 0,
  };

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-gray-100 rounded-lg">
            <Camera className="w-5 h-5 text-gray-600" />
          </div>
          <div>
            <p className="text-2xl font-bold">{stats.total}</p>
            <p className="text-sm text-gray-500">Total Items</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-green-100 rounded-lg">
            <Camera className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <p className="text-2xl font-bold">{stats.available}</p>
            <p className="text-sm text-gray-500">Available</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-yellow-100 rounded-lg">
            <Calendar className="w-5 h-5 text-yellow-600" />
          </div>
          <div>
            <p className="text-2xl font-bold">{stats.inUse}</p>
            <p className="text-sm text-gray-500">In Use</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-purple-100 rounded-lg">
            <AlertCircle className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <p className="text-2xl font-bold">{stats.maintenance}</p>
            <p className="text-sm text-gray-500">Maintenance</p>
          </div>
        </Card>
      </div>

      {/* Filters and Actions */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search equipment..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 w-64 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">All Categories</option>
            {categoryOptions.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Equipment
        </Button>
      </div>

      {/* Equipment Table */}
      <Card padding="none">
        <Table
          columns={columns}
          data={filteredEquipment || []}
          keyExtractor={(e) => e.id}
          isLoading={isLoading}
          emptyMessage="No equipment found"
        />
      </Card>

      {/* Add Equipment Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Equipment" size="lg">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Equipment Name" name="name" required placeholder="e.g., RED Komodo 6K" />
            <Input label="Asset Code" name="code" required placeholder="e.g., CAM-001" />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <Select
              label="Category"
              name="category"
              options={categoryOptions}
              placeholder="Select category"
              required
            />
            <Input label="Brand" name="brand" placeholder="e.g., RED" />
            <Input label="Model" name="model" placeholder="e.g., Komodo 6K" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Serial Number" name="serial_number" placeholder="Serial number" />
            <Input label="Storage Location" name="storage_location" placeholder="e.g., Warehouse A, Shelf 3" />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <Input label="Purchase Date" name="purchase_date" type="date" />
            <Input label="Purchase Price" name="purchase_price" type="number" placeholder="0.00" />
            <Input label="Daily Rental Rate" name="daily_rate" type="number" placeholder="0.00" />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Equipment</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
