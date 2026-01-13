import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: async (username: string, password: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data;
  },
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Projects API
export const projectsApi = {
  list: async (params?: { status?: string; client_id?: number }) => {
    const response = await api.get('/projects', { params });
    return response.data;
  },
  get: async (id: number) => {
    const response = await api.get(`/projects/${id}`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/projects', data);
    return response.data;
  },
  update: async (id: number, data: any) => {
    const response = await api.put(`/projects/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    await api.delete(`/projects/${id}`);
  },
};

// Tasks API
export const tasksApi = {
  listAll: async (params?: { status?: string; assignee_id?: number }) => {
    const response = await api.get('/projects/tasks/all', { params });
    return response.data;
  },
  listByProject: async (projectId: number, params?: { status?: string; sprint_id?: number }) => {
    const response = await api.get(`/projects/${projectId}/tasks`, { params });
    return response.data;
  },
  get: async (id: number) => {
    const response = await api.get(`/projects/tasks/${id}`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/projects/tasks', data);
    return response.data;
  },
  update: async (id: number, data: any) => {
    const response = await api.put(`/projects/tasks/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    await api.delete(`/projects/tasks/${id}`);
  },
};

// Sprints API
export const sprintsApi = {
  listByProject: async (projectId: number) => {
    const response = await api.get(`/projects/${projectId}/sprints`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/projects/sprints', data);
    return response.data;
  },
  update: async (id: number, data: any) => {
    const response = await api.put(`/projects/sprints/${id}`, data);
    return response.data;
  },
};

// CRM API
export const crmApi = {
  // Clients
  listClients: async (params?: { is_active?: boolean }) => {
    const response = await api.get('/crm/clients', { params });
    return response.data;
  },
  getClient: async (id: number) => {
    const response = await api.get(`/crm/clients/${id}`);
    return response.data;
  },
  createClient: async (data: any) => {
    const response = await api.post('/crm/clients', data);
    return response.data;
  },
  updateClient: async (id: number, data: any) => {
    const response = await api.put(`/crm/clients/${id}`, data);
    return response.data;
  },

  // Leads
  listLeads: async (params?: { status?: string; assigned_to_id?: number }) => {
    const response = await api.get('/crm/leads', { params });
    return response.data;
  },
  createLead: async (data: any) => {
    const response = await api.post('/crm/leads', data);
    return response.data;
  },
  updateLead: async (id: number, data: any) => {
    const response = await api.put(`/crm/leads/${id}`, data);
    return response.data;
  },

  // Deals
  listDeals: async (params?: { stage?: string; client_id?: number }) => {
    const response = await api.get('/crm/deals', { params });
    return response.data;
  },
  createDeal: async (data: any) => {
    const response = await api.post('/crm/deals', data);
    return response.data;
  },
  updateDeal: async (id: number, data: any) => {
    const response = await api.put(`/crm/deals/${id}`, data);
    return response.data;
  },

  // Contacts
  listContacts: async (params?: { client_id?: number }) => {
    const response = await api.get('/crm/contacts', { params });
    return response.data;
  },
  createContact: async (data: any) => {
    const response = await api.post('/crm/contacts', data);
    return response.data;
  },
};

// HR API
export const hrApi = {
  // Departments
  listDepartments: async () => {
    const response = await api.get('/hr/departments');
    return response.data;
  },
  createDepartment: async (data: any) => {
    const response = await api.post('/hr/departments', data);
    return response.data;
  },
  updateDepartment: async (id: number, data: any) => {
    const response = await api.put(`/hr/departments/${id}`, data);
    return response.data;
  },

  // Employees
  listEmployees: async (params?: { department_id?: number }) => {
    const response = await api.get('/hr/employees', { params });
    return response.data;
  },
  getEmployee: async (id: number) => {
    const response = await api.get(`/hr/employees/${id}`);
    return response.data;
  },
  createEmployee: async (data: any) => {
    const response = await api.post('/hr/employees', data);
    return response.data;
  },
  updateEmployee: async (id: number, data: any) => {
    const response = await api.put(`/hr/employees/${id}`, data);
    return response.data;
  },

  // Leave Requests
  listLeaveRequests: async (params?: { status?: string; employee_id?: number }) => {
    const response = await api.get('/hr/leave-requests', { params });
    return response.data;
  },
  createLeaveRequest: async (data: any) => {
    const response = await api.post('/hr/leave-requests', data);
    return response.data;
  },
  updateLeaveRequest: async (id: number, data: any) => {
    const response = await api.put(`/hr/leave-requests/${id}`, data);
    return response.data;
  },
};

// Accounting API
export const accountingApi = {
  // Invoices
  listInvoices: async (params?: { status?: string; client_id?: number; project_id?: number }) => {
    const response = await api.get('/accounting/invoices', { params });
    return response.data;
  },
  getInvoice: async (id: number) => {
    const response = await api.get(`/accounting/invoices/${id}`);
    return response.data;
  },
  createInvoice: async (data: any) => {
    const response = await api.post('/accounting/invoices', data);
    return response.data;
  },
  updateInvoice: async (id: number, data: any) => {
    const response = await api.put(`/accounting/invoices/${id}`, data);
    return response.data;
  },
  recordPayment: async (invoiceId: number, data: any) => {
    const response = await api.post(`/accounting/invoices/${invoiceId}/payments`, data);
    return response.data;
  },

  // Expenses
  listExpenses: async (params?: { status?: string; project_id?: number }) => {
    const response = await api.get('/accounting/expenses', { params });
    return response.data;
  },
  createExpense: async (data: any) => {
    const response = await api.post('/accounting/expenses', data);
    return response.data;
  },
  updateExpense: async (id: number, data: any) => {
    const response = await api.put(`/accounting/expenses/${id}`, data);
    return response.data;
  },

  // Budgets
  listBudgets: async (params?: { project_id?: number }) => {
    const response = await api.get('/accounting/budgets', { params });
    return response.data;
  },
  createBudget: async (data: any) => {
    const response = await api.post('/accounting/budgets', data);
    return response.data;
  },
};

// Equipment API
export const equipmentApi = {
  list: async (params?: { category?: string; status?: string; is_available?: boolean }) => {
    const response = await api.get('/equipment', { params });
    return response.data;
  },
  get: async (id: number) => {
    const response = await api.get(`/equipment/${id}`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/equipment', data);
    return response.data;
  },
  update: async (id: number, data: any) => {
    const response = await api.put(`/equipment/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    await api.delete(`/equipment/${id}`);
  },

  // Bookings
  listBookings: async (params?: { status?: string; equipment_id?: number }) => {
    const response = await api.get('/equipment/bookings/all', { params });
    return response.data;
  },
  createBooking: async (data: any) => {
    const response = await api.post('/equipment/bookings', data);
    return response.data;
  },
  updateBooking: async (id: number, data: any) => {
    const response = await api.put(`/equipment/bookings/${id}`, data);
    return response.data;
  },
};

// Production API
export const productionApi = {
  // Locations
  listLocations: async (params?: { location_type?: string }) => {
    const response = await api.get('/production/locations', { params });
    return response.data;
  },
  createLocation: async (data: any) => {
    const response = await api.post('/production/locations', data);
    return response.data;
  },
  updateLocation: async (id: number, data: any) => {
    const response = await api.put(`/production/locations/${id}`, data);
    return response.data;
  },

  // Schedules
  listSchedules: async (params?: { project_id?: number; status?: string }) => {
    const response = await api.get('/production/schedules', { params });
    return response.data;
  },
  getSchedule: async (id: number) => {
    const response = await api.get(`/production/schedules/${id}`);
    return response.data;
  },
  createSchedule: async (data: any) => {
    const response = await api.post('/production/schedules', data);
    return response.data;
  },
  updateSchedule: async (id: number, data: any) => {
    const response = await api.put(`/production/schedules/${id}`, data);
    return response.data;
  },

  // Crew
  listCrew: async (scheduleId: number) => {
    const response = await api.get(`/production/schedules/${scheduleId}/crew`);
    return response.data;
  },
  createCrewAssignment: async (data: any) => {
    const response = await api.post('/production/crew', data);
    return response.data;
  },
};

// Dashboard API
export const dashboardApi = {
  getStats: async () => {
    const response = await api.get('/dashboard/stats');
    return response.data;
  },
  getRecentActivity: async () => {
    const response = await api.get('/dashboard/recent-activity');
    return response.data;
  },
  getMyTasks: async () => {
    const response = await api.get('/dashboard/my-tasks');
    return response.data;
  },
};

// Users API
export const usersApi = {
  list: async () => {
    const response = await api.get('/users');
    return response.data;
  },
  get: async (id: number) => {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/users', data);
    return response.data;
  },
  update: async (id: number, data: any) => {
    const response = await api.put(`/users/${id}`, data);
    return response.data;
  },
};
