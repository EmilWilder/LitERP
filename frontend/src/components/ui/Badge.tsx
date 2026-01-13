import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'purple';
  size?: 'sm' | 'md';
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  size = 'sm',
}) => {
  const variants = {
    default: 'bg-gray-100 text-gray-700',
    success: 'bg-green-100 text-green-700',
    warning: 'bg-yellow-100 text-yellow-700',
    danger: 'bg-red-100 text-red-700',
    info: 'bg-blue-100 text-blue-700',
    purple: 'bg-purple-100 text-purple-700',
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
  };

  return (
    <span className={`inline-flex items-center font-medium rounded-full ${variants[variant]} ${sizes[size]}`}>
      {children}
    </span>
  );
};

// Helper function to get badge variant based on status
export const getStatusBadgeVariant = (status: string): BadgeProps['variant'] => {
  const statusVariants: Record<string, BadgeProps['variant']> = {
    // Task statuses
    backlog: 'default',
    todo: 'info',
    in_progress: 'warning',
    in_review: 'purple',
    blocked: 'danger',
    done: 'success',
    
    // Project statuses
    planning: 'default',
    pre_production: 'info',
    production: 'warning',
    post_production: 'purple',
    review: 'info',
    completed: 'success',
    on_hold: 'warning',
    cancelled: 'danger',
    
    // Lead statuses
    new: 'info',
    contacted: 'purple',
    qualified: 'warning',
    proposal_sent: 'info',
    negotiation: 'warning',
    won: 'success',
    lost: 'danger',
    
    // Deal stages
    discovery: 'info',
    proposal: 'purple',
    contract: 'warning',
    closed_won: 'success',
    closed_lost: 'danger',
    
    // Invoice statuses
    draft: 'default',
    sent: 'info',
    viewed: 'purple',
    partial: 'warning',
    paid: 'success',
    overdue: 'danger',
    
    // Expense statuses
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    reimbursed: 'info',
    
    // Equipment statuses
    available: 'success',
    in_use: 'warning',
    reserved: 'info',
    maintenance: 'purple',
    damaged: 'danger',
    retired: 'default',
    
    // Schedule statuses
    tentative: 'default',
    confirmed: 'success',
    postponed: 'warning',
  };

  return statusVariants[status] || 'default';
};
