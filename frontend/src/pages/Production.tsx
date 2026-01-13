import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { NavLink, Routes, Route } from 'react-router-dom';
import { Plus, Calendar, MapPin, Clock, Users } from 'lucide-react';
import { Card, Button, Input, Badge, getStatusBadgeVariant, Modal, Select, Table } from '../components/ui';
import { productionApi, projectsApi } from '../services/api';
import { ProductionSchedule, Project } from '../types';
import { format } from 'date-fns';

const ProductionNav: React.FC = () => (
  <div className="flex gap-1 mb-6 bg-gray-100 p-1 rounded-lg w-fit">
    {[
      { to: '/production', label: 'Schedules', icon: Calendar, end: true },
      { to: '/production/locations', label: 'Locations', icon: MapPin },
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

// Schedules Page
const SchedulesPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: schedules, isLoading } = useQuery<ProductionSchedule[]>({
    queryKey: ['schedules'],
    queryFn: () => productionApi.listSchedules(),
  });

  const { data: projects } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: () => projectsApi.list(),
  });

  const { data: locations } = useQuery({
    queryKey: ['locations'],
    queryFn: () => productionApi.listLocations(),
  });

  const createMutation = useMutation({
    mutationFn: productionApi.createSchedule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      project_id: parseInt(formData.get('project_id') as string),
      title: formData.get('title'),
      date: formData.get('date'),
      shoot_type: formData.get('shoot_type'),
      location_id: parseInt(formData.get('location_id') as string) || null,
      call_time: formData.get('call_time') || null,
      start_time: formData.get('start_time') || null,
      end_time: formData.get('end_time') || null,
      general_notes: formData.get('general_notes'),
    });
  };

  const shootTypeOptions = [
    { value: 'studio', label: 'Studio' },
    { value: 'on_location', label: 'On Location' },
    { value: 'green_screen', label: 'Green Screen' },
    { value: 'interview', label: 'Interview' },
    { value: 'b_roll', label: 'B-Roll' },
    { value: 'aerial', label: 'Aerial' },
    { value: 'live_event', label: 'Live Event' },
    { value: 'other', label: 'Other' },
  ];

  // Group schedules by date
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const upcomingSchedules = schedules?.filter(s => new Date(s.date) >= today).sort((a, b) => 
    new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Production Schedules</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          New Shoot
        </Button>
      </div>

      {/* Calendar View */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : upcomingSchedules?.length === 0 ? (
          <Card className="text-center py-12">
            <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900">No upcoming shoots</h3>
            <p className="text-gray-500 mt-1">Schedule your first production shoot</p>
          </Card>
        ) : (
          upcomingSchedules?.map((schedule) => (
            <Card key={schedule.id} className="flex items-start gap-6">
              <div className="flex-shrink-0 w-20 text-center">
                <div className="text-3xl font-bold text-primary-600">
                  {format(new Date(schedule.date), 'd')}
                </div>
                <div className="text-sm text-gray-500">
                  {format(new Date(schedule.date), 'MMM yyyy')}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  {format(new Date(schedule.date), 'EEEE')}
                </div>
              </div>
              <div className="flex-1 border-l pl-6">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-gray-900">{schedule.title}</h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {projects?.find(p => p.id === schedule.project_id)?.name || 'Unknown Project'}
                    </p>
                  </div>
                  <Badge variant={getStatusBadgeVariant(schedule.status)}>
                    {schedule.status}
                  </Badge>
                </div>
                <div className="flex items-center gap-6 mt-4 text-sm text-gray-600">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4" />
                    {schedule.call_time ? `Call: ${schedule.call_time}` : 'TBD'}
                    {schedule.start_time && ` • Start: ${schedule.start_time}`}
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4" />
                    {locations?.find((l: any) => l.id === schedule.location_id)?.name || 'Location TBD'}
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="info">{schedule.shoot_type.replace('_', ' ')}</Badge>
                  </div>
                </div>
                {schedule.general_notes && (
                  <p className="text-sm text-gray-500 mt-3">{schedule.general_notes}</p>
                )}
              </div>
            </Card>
          ))
        )}
      </div>

      {/* New Shoot Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Schedule New Shoot" size="lg">
        <form onSubmit={handleCreate} className="space-y-4">
          <Select
            label="Project"
            name="project_id"
            options={projects?.map(p => ({ value: p.id.toString(), label: `${p.code} - ${p.name}` })) || []}
            placeholder="Select project"
            required
          />
          <Input label="Shoot Title" name="title" required placeholder="e.g., Day 1 - Office Scenes" />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Date" name="date" type="date" required />
            <Select
              label="Shoot Type"
              name="shoot_type"
              options={shootTypeOptions}
              placeholder="Select type"
            />
          </div>
          <Select
            label="Location"
            name="location_id"
            options={locations?.map((l: any) => ({ value: l.id.toString(), label: l.name })) || []}
            placeholder="Select location"
          />
          <div className="grid grid-cols-3 gap-4">
            <Input label="Call Time" name="call_time" type="time" />
            <Input label="Start Time" name="start_time" type="time" />
            <Input label="End Time" name="end_time" type="time" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
            <textarea
              name="general_notes"
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
              placeholder="General notes for the crew..."
            />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Schedule Shoot</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

// Locations Page
const LocationsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: locations, isLoading } = useQuery({
    queryKey: ['locations'],
    queryFn: () => productionApi.listLocations(),
  });

  const createMutation = useMutation({
    mutationFn: productionApi.createLocation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['locations'] });
      setShowModal(false);
    },
  });

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      name: formData.get('name'),
      location_type: formData.get('location_type'),
      address_line1: formData.get('address_line1'),
      city: formData.get('city'),
      state: formData.get('state'),
      country: formData.get('country'),
      contact_name: formData.get('contact_name'),
      contact_phone: formData.get('contact_phone'),
      rental_rate: parseFloat(formData.get('rental_rate') as string) || null,
      has_power: formData.get('has_power') === 'on',
      has_parking: formData.get('has_parking') === 'on',
      permit_required: formData.get('permit_required') === 'on',
    });
  };

  const columns = [
    { key: 'name', header: 'Name', render: (l: any) => <span className="font-medium">{l.name}</span> },
    { key: 'location_type', header: 'Type', render: (l: any) => <Badge>{l.location_type}</Badge> },
    { key: 'city', header: 'City', render: (l: any) => `${l.city || '-'}${l.state ? `, ${l.state}` : ''}` },
    { key: 'contact_name', header: 'Contact', render: (l: any) => l.contact_name || '-' },
    { key: 'rental_rate', header: 'Rate', render: (l: any) => l.rental_rate ? `$${l.rental_rate}/day` : '-' },
    { key: 'amenities', header: 'Amenities', render: (l: any) => (
      <div className="flex gap-1">
        {l.has_power && <Badge size="sm">Power</Badge>}
        {l.has_parking && <Badge size="sm">Parking</Badge>}
        {l.has_wifi && <Badge size="sm">WiFi</Badge>}
      </div>
    )},
    { key: 'permit_required', header: 'Permit', render: (l: any) => (
      <Badge variant={l.permit_required ? 'warning' : 'success'}>
        {l.permit_required ? 'Required' : 'Not Required'}
      </Badge>
    )},
  ];

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Locations</h2>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Location
        </Button>
      </div>
      <Card padding="none">
        <Table columns={columns} data={locations || []} keyExtractor={(l) => l.id} isLoading={isLoading} />
      </Card>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Add New Location" size="lg">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Location Name" name="name" required placeholder="e.g., Downtown Studio" />
            <Select
              label="Type"
              name="location_type"
              options={[
                { value: 'studio', label: 'Studio' },
                { value: 'office', label: 'Office' },
                { value: 'outdoor', label: 'Outdoor' },
                { value: 'residential', label: 'Residential' },
                { value: 'commercial', label: 'Commercial' },
                { value: 'industrial', label: 'Industrial' },
                { value: 'natural', label: 'Natural' },
                { value: 'other', label: 'Other' },
              ]}
            />
          </div>
          <Input label="Address" name="address_line1" placeholder="Street address" />
          <div className="grid grid-cols-3 gap-4">
            <Input label="City" name="city" />
            <Input label="State" name="state" />
            <Input label="Country" name="country" />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <Input label="Contact Name" name="contact_name" />
            <Input label="Contact Phone" name="contact_phone" />
            <Input label="Daily Rate" name="rental_rate" type="number" placeholder="0.00" />
          </div>
          <div className="flex items-center gap-6">
            <label className="flex items-center gap-2">
              <input type="checkbox" name="has_power" className="rounded border-gray-300" defaultChecked />
              <span className="text-sm">Has Power</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" name="has_parking" className="rounded border-gray-300" />
              <span className="text-sm">Has Parking</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" name="permit_required" className="rounded border-gray-300" />
              <span className="text-sm">Permit Required</span>
            </label>
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Add Location</Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

export const Production: React.FC = () => {
  return (
    <div>
      <ProductionNav />
      <Routes>
        <Route index element={<SchedulesPage />} />
        <Route path="locations" element={<LocationsPage />} />
      </Routes>
    </div>
  );
};
