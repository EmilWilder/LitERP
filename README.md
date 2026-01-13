# LitERP - Video Production ERP

A lightweight, scalable Enterprise Resource Planning (ERP) system specifically designed for video production companies. Built with modern technologies for optimal performance and user experience.

![LitERP](https://img.shields.io/badge/LitERP-Video%20Production-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![React](https://img.shields.io/badge/React-18+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

### 📁 Project Management (Jira-like)
- **Kanban Board** - Drag-and-drop task management
- **Sprints** - Time-boxed iterations for agile workflows
- **Task Types** - Tasks, stories, epics, bugs, milestones
- **Priority Levels** - Lowest to highest priority tracking
- **Comments** - Threaded discussions on tasks
- **Attachments** - File attachments for tasks
- **Video Production Stages** - Pre-production, production, post-production tracking

### 👥 Human Resources (HR)
- **Employee Management** - Complete employee profiles
- **Departments** - Organizational structure
- **Leave Requests** - Time-off management with approvals
- **Attendance Tracking** - Check-in/check-out with location
- **Skills & Certifications** - Track crew capabilities
- **Employment Types** - Full-time, part-time, contract, freelance

### 🤝 Customer Relationship Management (CRM)
- **Clients** - Client database with contact info
- **Contacts** - Individual contact management
- **Leads** - Lead tracking and conversion
- **Deals** - Sales pipeline with stages
- **Interactions** - Call, email, meeting logs
- **Client Types** - Agency, brand, broadcaster, etc.

### 💰 Accounting
- **Invoices** - Create and track invoices
- **Line Items** - Detailed invoice items
- **Payments** - Payment recording and tracking
- **Expenses** - Expense management with approvals
- **Budgets** - Project budget tracking
- **Categories** - Video production specific expense categories

### 📷 Equipment & Inventory
- **Equipment Catalog** - Full asset management
- **Bookings** - Equipment reservation system
- **Maintenance** - Service and repair tracking
- **Categories** - Cameras, lenses, lighting, audio, etc.
- **Status Tracking** - Available, in-use, maintenance, retired
- **Rental Rates** - Daily and weekly rates

### 🎬 Production Scheduling
- **Shoot Days** - Schedule production days
- **Locations** - Location database with details
- **Crew Assignments** - Assign crew to shoots
- **Call Sheets** - Call times and notes
- **Shoot Types** - Studio, on-location, aerial, etc.
- **Weather Backup** - Alternative shoot dates

### 📊 Dashboard & Analytics
- **Overview Stats** - Key metrics at a glance
- **My Tasks** - Personal task list
- **Recent Activity** - Latest updates
- **Pipeline Value** - Sales pipeline summary

## Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy 2.0** - Async ORM with type hints
- **Pydantic v2** - Data validation
- **SQLite/PostgreSQL** - Database (SQLite for dev, PostgreSQL for prod)
- **JWT** - Authentication with JSON Web Tokens
- **Bcrypt** - Secure password hashing

### Frontend
- **React 18** - UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **React Query** - Server state management
- **Zustand** - Client state management
- **React Router** - Client-side routing
- **Lucide Icons** - Beautiful icons
- **date-fns** - Date formatting

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Default Credentials
- **Username:** `admin`
- **Password:** `admin123`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

### Projects
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/{id}` - Get project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Archive project

### Tasks
- `GET /api/v1/projects/tasks/all` - List all tasks
- `GET /api/v1/projects/{id}/tasks` - List project tasks
- `POST /api/v1/projects/tasks` - Create task
- `PUT /api/v1/projects/tasks/{id}` - Update task
- `DELETE /api/v1/projects/tasks/{id}` - Delete task

### CRM
- `GET /api/v1/crm/clients` - List clients
- `POST /api/v1/crm/clients` - Create client
- `GET /api/v1/crm/leads` - List leads
- `POST /api/v1/crm/leads` - Create lead
- `GET /api/v1/crm/deals` - List deals
- `POST /api/v1/crm/deals` - Create deal

### HR
- `GET /api/v1/hr/departments` - List departments
- `GET /api/v1/hr/employees` - List employees
- `GET /api/v1/hr/leave-requests` - List leave requests

### Accounting
- `GET /api/v1/accounting/invoices` - List invoices
- `POST /api/v1/accounting/invoices` - Create invoice
- `GET /api/v1/accounting/expenses` - List expenses
- `POST /api/v1/accounting/expenses` - Create expense

### Equipment
- `GET /api/v1/equipment` - List equipment
- `POST /api/v1/equipment` - Add equipment
- `GET /api/v1/equipment/bookings/all` - List bookings
- `POST /api/v1/equipment/bookings` - Create booking

### Production
- `GET /api/v1/production/schedules` - List schedules
- `POST /api/v1/production/schedules` - Create schedule
- `GET /api/v1/production/locations` - List locations
- `POST /api/v1/production/locations` - Create location

### Dashboard
- `GET /api/v1/dashboard/stats` - Get statistics
- `GET /api/v1/dashboard/recent-activity` - Get recent activity
- `GET /api/v1/dashboard/my-tasks` - Get user's tasks

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/       # API route handlers
│   │   ├── core/             # Config, security, database
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── main.py           # FastAPI application
│   ├── tests/                # Backend tests
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── layout/       # Layout components
│   │   │   └── ui/           # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service layer
│   │   ├── store/            # Zustand stores
│   │   ├── types/            # TypeScript types
│   │   └── App.tsx           # Main app component
│   ├── index.html
│   └── package.json
│
└── README.md
```

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key-min-32-characters
DATABASE_URL=sqlite+aiosqlite:///./literp.db
# For PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://user:pass@localhost/literp
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Scaling for Production

### Database
Switch from SQLite to PostgreSQL for production:
```python
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/literp
```

### Deployment
- Use Gunicorn with Uvicorn workers for the backend
- Build the frontend with `npm run build` and serve with nginx
- Use Docker for containerization
- Consider using Redis for caching and Celery for background tasks

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.
