import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Search, MoreVertical, Calendar, Users } from 'lucide-react';
import { Card, Button, Input, Badge, getStatusBadgeVariant, Modal, Select } from '../components/ui';
import { projectsApi, tasksApi } from '../services/api';
import { Project, Task, TaskStatus } from '../types';
import { useAuthStore } from '../store/authStore';
import { format } from 'date-fns';

const taskStatusColumns: { status: TaskStatus; label: string; color: string }[] = [
  { status: 'backlog', label: 'Backlog', color: 'bg-gray-100' },
  { status: 'todo', label: 'To Do', color: 'bg-blue-100' },
  { status: 'in_progress', label: 'In Progress', color: 'bg-yellow-100' },
  { status: 'in_review', label: 'In Review', color: 'bg-purple-100' },
  { status: 'done', label: 'Done', color: 'bg-green-100' },
];

const projectTypeOptions = [
  { value: 'commercial', label: 'Commercial' },
  { value: 'corporate', label: 'Corporate' },
  { value: 'documentary', label: 'Documentary' },
  { value: 'music_video', label: 'Music Video' },
  { value: 'short_film', label: 'Short Film' },
  { value: 'feature_film', label: 'Feature Film' },
  { value: 'tv_series', label: 'TV Series' },
  { value: 'social_media', label: 'Social Media' },
  { value: 'live_event', label: 'Live Event' },
  { value: 'animation', label: 'Animation' },
  { value: 'other', label: 'Other' },
];

export const Projects: React.FC = () => {
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const queryClient = useQueryClient();
  const { user } = useAuthStore();

  const { data: projects, isLoading: projectsLoading } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: () => projectsApi.list(),
  });

  const { data: tasks, isLoading: tasksLoading } = useQuery<Task[]>({
    queryKey: ['tasks', selectedProject?.id],
    queryFn: () => selectedProject ? tasksApi.listByProject(selectedProject.id) : Promise.resolve([]),
    enabled: !!selectedProject,
  });

  const createProjectMutation = useMutation({
    mutationFn: projectsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      setShowProjectModal(false);
    },
  });

  const createTaskMutation = useMutation({
    mutationFn: tasksApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setShowTaskModal(false);
    },
  });

  const updateTaskMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => tasksApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const filteredProjects = projects?.filter(p =>
    p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    p.code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCreateProject = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createProjectMutation.mutate({
      name: formData.get('name'),
      code: formData.get('code'),
      project_type: formData.get('project_type'),
      description: formData.get('description'),
      estimated_budget: parseFloat(formData.get('estimated_budget') as string) || 0,
    });
  };

  const handleCreateTask = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createTaskMutation.mutate({
      project_id: selectedProject?.id,
      title: formData.get('title'),
      description: formData.get('description'),
      priority: formData.get('priority'),
      created_by_id: user?.id,
    });
  };

  const handleDragStart = (e: React.DragEvent, taskId: number) => {
    e.dataTransfer.setData('taskId', taskId.toString());
  };

  const handleDrop = (e: React.DragEvent, newStatus: TaskStatus) => {
    e.preventDefault();
    const taskId = parseInt(e.dataTransfer.getData('taskId'));
    updateTaskMutation.mutate({ id: taskId, data: { status: newStatus } });
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 w-64 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>
        <Button onClick={() => setShowProjectModal(true)}>
          <Plus className="w-4 h-4 mr-2" />
          New Project
        </Button>
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* Projects List */}
        <div className="col-span-3">
          <Card padding="sm">
            <h3 className="font-semibold text-gray-900 mb-4 px-2">Projects</h3>
            <div className="space-y-1 max-h-[calc(100vh-280px)] overflow-y-auto">
              {projectsLoading ? (
                <div className="text-center py-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mx-auto"></div>
                </div>
              ) : filteredProjects?.length === 0 ? (
                <p className="text-sm text-gray-500 text-center py-4">No projects found</p>
              ) : (
                filteredProjects?.map((project) => (
                  <button
                    key={project.id}
                    onClick={() => setSelectedProject(project)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedProject?.id === project.id
                        ? 'bg-primary-50 border border-primary-200'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono text-gray-500">{project.code}</span>
                      <Badge variant={getStatusBadgeVariant(project.status)} size="sm">
                        {project.status.replace('_', ' ')}
                      </Badge>
                    </div>
                    <p className="font-medium text-gray-900 mt-1 truncate">{project.name}</p>
                    <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                      <span className="capitalize">{project.project_type.replace('_', ' ')}</span>
                      <span>•</span>
                      <span>{project.progress_percentage}%</span>
                    </div>
                  </button>
                ))
              )}
            </div>
          </Card>
        </div>

        {/* Kanban Board */}
        <div className="col-span-9">
          {selectedProject ? (
            <div>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">{selectedProject.name}</h2>
                  <p className="text-sm text-gray-500">{selectedProject.description || 'No description'}</p>
                </div>
                <Button onClick={() => setShowTaskModal(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Add Task
                </Button>
              </div>

              {/* Kanban Columns */}
              <div className="flex gap-4 overflow-x-auto pb-4">
                {taskStatusColumns.map((column) => {
                  const columnTasks = tasks?.filter((t) => t.status === column.status) || [];
                  return (
                    <div
                      key={column.status}
                      className="flex-shrink-0 w-72"
                      onDrop={(e) => handleDrop(e, column.status)}
                      onDragOver={handleDragOver}
                    >
                      <div className={`${column.color} rounded-t-lg px-3 py-2`}>
                        <div className="flex items-center justify-between">
                          <span className="font-medium text-sm text-gray-700">{column.label}</span>
                          <span className="text-xs bg-white px-2 py-0.5 rounded-full text-gray-600">
                            {columnTasks.length}
                          </span>
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded-b-lg p-2 min-h-[400px] space-y-2">
                        {tasksLoading ? (
                          <div className="text-center py-4">
                            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mx-auto"></div>
                          </div>
                        ) : (
                          columnTasks.map((task) => (
                            <div
                              key={task.id}
                              draggable
                              onDragStart={(e) => handleDragStart(e, task.id)}
                              className="bg-white p-3 rounded-lg shadow-sm border border-gray-100 cursor-move hover:shadow-md transition-shadow"
                            >
                              <div className="flex items-start justify-between">
                                <span className="text-xs font-mono text-gray-500">{task.task_key}</span>
                                <Badge
                                  variant={
                                    task.priority === 'highest' || task.priority === 'high'
                                      ? 'danger'
                                      : task.priority === 'medium'
                                      ? 'warning'
                                      : 'default'
                                  }
                                  size="sm"
                                >
                                  {task.priority}
                                </Badge>
                              </div>
                              <p className="font-medium text-gray-900 mt-2 text-sm">{task.title}</p>
                              {task.due_date && (
                                <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
                                  <Calendar className="w-3 h-3" />
                                  {format(new Date(task.due_date), 'MMM d')}
                                </div>
                              )}
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <Card className="flex items-center justify-center h-96">
              <div className="text-center">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-medium text-gray-900">Select a Project</h3>
                <p className="text-gray-500 mt-1">Choose a project from the list to view its tasks</p>
              </div>
            </Card>
          )}
        </div>
      </div>

      {/* Create Project Modal */}
      <Modal isOpen={showProjectModal} onClose={() => setShowProjectModal(false)} title="Create New Project">
        <form onSubmit={handleCreateProject} className="space-y-4">
          <Input label="Project Name" name="name" required placeholder="e.g., Nike Commercial 2026" />
          <Input label="Project Code" name="code" required placeholder="e.g., NIKE-001" />
          <Select
            label="Project Type"
            name="project_type"
            options={projectTypeOptions}
            placeholder="Select type"
            required
          />
          <Input
            label="Estimated Budget"
            name="estimated_budget"
            type="number"
            placeholder="0.00"
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              name="description"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="Project description..."
            />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowProjectModal(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={createProjectMutation.isPending}>
              Create Project
            </Button>
          </div>
        </form>
      </Modal>

      {/* Create Task Modal */}
      <Modal isOpen={showTaskModal} onClose={() => setShowTaskModal(false)} title="Create New Task">
        <form onSubmit={handleCreateTask} className="space-y-4">
          <Input label="Task Title" name="title" required placeholder="e.g., Script review" />
          <Select
            label="Priority"
            name="priority"
            options={[
              { value: 'lowest', label: 'Lowest' },
              { value: 'low', label: 'Low' },
              { value: 'medium', label: 'Medium' },
              { value: 'high', label: 'High' },
              { value: 'highest', label: 'Highest' },
            ]}
            placeholder="Select priority"
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              name="description"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              placeholder="Task description..."
            />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setShowTaskModal(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={createTaskMutation.isPending}>
              Create Task
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
