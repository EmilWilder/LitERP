// User types
export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  role: UserRole;
  is_active: boolean;
  is_superuser: boolean;
  avatar_url: string | null;
  phone: string | null;
  created_at: string;
}

export type UserRole = 
  | 'admin' | 'manager' | 'producer' | 'editor' 
  | 'cameraman' | 'accountant' | 'hr' | 'sales' | 'employee';

// Project types
export interface Project {
  id: number;
  name: string;
  code: string;
  description: string | null;
  project_type: ProjectType;
  status: ProjectStatus;
  client_id: number | null;
  project_manager_id: number | null;
  director_id: number | null;
  producer_id: number | null;
  start_date: string | null;
  target_end_date: string | null;
  actual_end_date: string | null;
  estimated_budget: number;
  actual_budget: number;
  video_format: string | null;
  aspect_ratio: string | null;
  duration_minutes: number | null;
  progress_percentage: number;
  is_archived: boolean;
  created_at: string;
}

export type ProjectStatus = 
  | 'planning' | 'pre_production' | 'production' 
  | 'post_production' | 'review' | 'completed' 
  | 'on_hold' | 'cancelled';

export type ProjectType = 
  | 'commercial' | 'corporate' | 'documentary' 
  | 'music_video' | 'short_film' | 'feature_film' 
  | 'tv_series' | 'social_media' | 'live_event' 
  | 'animation' | 'other';

// Task types
export interface Task {
  id: number;
  project_id: number;
  sprint_id: number | null;
  parent_task_id: number | null;
  task_key: string;
  title: string;
  description: string | null;
  task_type: TaskType;
  status: TaskStatus;
  priority: TaskPriority;
  assignee_id: number | null;
  created_by_id: number;
  estimated_hours: number | null;
  logged_hours: number;
  due_date: string | null;
  started_at: string | null;
  completed_at: string | null;
  stage: string | null;
  scene_number: string | null;
  position: number;
  labels: string | null;
  created_at: string;
}

export type TaskStatus = 'backlog' | 'todo' | 'in_progress' | 'in_review' | 'blocked' | 'done';
export type TaskPriority = 'lowest' | 'low' | 'medium' | 'high' | 'highest';
export type TaskType = 'task' | 'bug' | 'story' | 'epic' | 'subtask' | 'milestone';

// Sprint types
export interface Sprint {
  id: number;
  project_id: number;
  name: string;
  goal: string | null;
  start_date: string;
  end_date: string;
  is_active: boolean;
  is_completed: boolean;
  created_at: string;
}

// Client types
export interface Client {
  id: number;
  name: string;
  code: string;
  client_type: ClientType;
  email: string | null;
  phone: string | null;
  website: string | null;
  city: string | null;
  country: string | null;
  industry: string | null;
  account_manager_id: number | null;
  payment_terms: number;
  is_active: boolean;
  created_at: string;
}

export type ClientType = 
  | 'agency' | 'brand' | 'production_company' 
  | 'broadcaster' | 'streaming_platform' 
  | 'individual' | 'non_profit' | 'government' | 'other';

// Lead types
export interface Lead {
  id: number;
  title: string;
  description: string | null;
  source: LeadSource;
  status: LeadStatus;
  contact_id: number | null;
  contact_name: string | null;
  contact_email: string | null;
  company_name: string | null;
  estimated_value: number | null;
  probability: number;
  assigned_to_id: number | null;
  project_type_interest: string | null;
  next_follow_up: string | null;
  converted_to_deal_id: number | null;
  converted_at: string | null;
  created_at: string;
}

export type LeadStatus = 'new' | 'contacted' | 'qualified' | 'proposal_sent' | 'negotiation' | 'won' | 'lost';
export type LeadSource = 'website' | 'referral' | 'social_media' | 'cold_call' | 'email_campaign' | 'trade_show' | 'partnership' | 'repeat_client' | 'other';

// Deal types
export interface Deal {
  id: number;
  name: string;
  description: string | null;
  client_id: number;
  contact_id: number | null;
  stage: DealStage;
  amount: number;
  probability: number;
  expected_revenue: number;
  expected_close_date: string | null;
  actual_close_date: string | null;
  owner_id: number | null;
  project_id: number | null;
  created_at: string;
}

export type DealStage = 'discovery' | 'proposal' | 'negotiation' | 'contract' | 'closed_won' | 'closed_lost';

// Invoice types
export interface Invoice {
  id: number;
  invoice_number: string;
  client_id: number;
  project_id: number | null;
  status: InvoiceStatus;
  issue_date: string;
  due_date: string;
  subtotal: number;
  tax_rate: number;
  tax_amount: number;
  discount_percentage: number;
  discount_amount: number;
  total_amount: number;
  amount_paid: number;
  balance_due: number;
  currency: string;
  notes: string | null;
  terms: string | null;
  payment_terms: number;
  sent_at: string | null;
  viewed_at: string | null;
  created_at: string;
}

export type InvoiceStatus = 'draft' | 'sent' | 'viewed' | 'partial' | 'paid' | 'overdue' | 'cancelled';

// Expense types
export interface Expense {
  id: number;
  expense_number: string;
  project_id: number | null;
  employee_id: number | null;
  category: ExpenseCategory;
  description: string;
  amount: number;
  currency: string;
  expense_date: string;
  vendor_name: string | null;
  status: ExpenseStatus;
  is_reimbursable: boolean;
  approved_by_id: number | null;
  approved_at: string | null;
  reimbursed_at: string | null;
  submitted_by_id: number | null;
  created_at: string;
}

export type ExpenseCategory = 
  | 'equipment_rental' | 'talent' | 'crew' | 'location' 
  | 'catering' | 'transportation' | 'accommodation' 
  | 'post_production' | 'music_licensing' | 'props' 
  | 'wardrobe' | 'insurance' | 'permits' | 'software' 
  | 'marketing' | 'office' | 'utilities' | 'other';

export type ExpenseStatus = 'pending' | 'approved' | 'rejected' | 'reimbursed';

// Equipment types
export interface Equipment {
  id: number;
  name: string;
  code: string;
  category: EquipmentCategory;
  brand: string | null;
  model: string | null;
  serial_number: string | null;
  description: string | null;
  status: EquipmentStatus;
  condition_notes: string | null;
  purchase_date: string | null;
  purchase_price: number | null;
  current_value: number | null;
  storage_location: string | null;
  current_location: string | null;
  is_rentable: boolean;
  daily_rate: number | null;
  weekly_rate: number | null;
  last_maintenance_date: string | null;
  next_maintenance_date: string | null;
  image_url: string | null;
  is_active: boolean;
  created_at: string;
}

export type EquipmentCategory = 
  | 'camera' | 'lens' | 'lighting' | 'audio' 
  | 'grip' | 'support' | 'drone' | 'monitor' 
  | 'storage' | 'computer' | 'software' | 'vehicle' | 'other';

export type EquipmentStatus = 'available' | 'in_use' | 'reserved' | 'maintenance' | 'damaged' | 'retired';

// Employee types
export interface Employee {
  id: number;
  user_id: number;
  employee_code: string;
  department_id: number | null;
  job_title: string;
  employment_type: EmploymentType;
  hire_date: string;
  date_of_birth: string | null;
  address: string | null;
  salary: number | null;
  skills: string | null;
  annual_leave_balance: number;
  sick_leave_balance: number;
  is_active: boolean;
  created_at: string;
}

export type EmploymentType = 'full_time' | 'part_time' | 'contract' | 'freelance' | 'intern';

// Department types
export interface Department {
  id: number;
  name: string;
  code: string;
  description: string | null;
  manager_id: number | null;
  budget: number;
  is_active: boolean;
  created_at: string;
}

// Production Schedule types
export interface ProductionSchedule {
  id: number;
  project_id: number;
  title: string;
  description: string | null;
  shoot_type: ShootType;
  status: ScheduleStatus;
  location_id: number | null;
  location_notes: string | null;
  date: string;
  call_time: string | null;
  start_time: string | null;
  end_time: string | null;
  wrap_time: string | null;
  weather_backup_date: string | null;
  scenes: string | null;
  shot_count: number | null;
  general_notes: string | null;
  production_manager_id: number | null;
  created_at: string;
}

export type ShootType = 
  | 'studio' | 'on_location' | 'green_screen' 
  | 'interview' | 'b_roll' | 'aerial' 
  | 'underwater' | 'live_event' | 'other';

export type ScheduleStatus = 
  | 'tentative' | 'confirmed' | 'in_progress' 
  | 'completed' | 'postponed' | 'cancelled';

// Dashboard types
export interface DashboardStats {
  projects: {
    active: number;
    completed: number;
  };
  tasks: {
    total: number;
    in_progress: number;
    completed: number;
  };
  crm: {
    active_clients: number;
    new_leads: number;
    open_deals: number;
    pipeline_value: number;
  };
  finance: {
    pending_invoices: number;
    pending_amount: number;
    overdue_invoices: number;
  };
  equipment: {
    available: number;
    in_use: number;
  };
  hr: {
    total_employees: number;
    pending_leave_requests: number;
  };
  production: {
    upcoming_shoots: number;
  };
}
