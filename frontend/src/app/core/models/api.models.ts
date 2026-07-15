export type UserRole = 'admin' | 'operator' | 'viewer';
export type MachineStatus = 'operational' | 'warning' | 'critical' | 'offline';
export type AlertSeverity = 'info' | 'warning' | 'critical';
export type AlertStatus = 'active' | 'acknowledged' | 'resolved';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: 'bearer';
  user: User;
}

export interface PageResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
}

export interface Machine {
  id: number;
  code: string;
  name: string;
  location: string;
  status: MachineStatus;
  temperature_celsius: number;
  vibration_mm_s: number;
  output_rate: number;
  efficiency_percent: number;
  last_seen_at: string;
  created_at: string;
  updated_at: string;
}

export interface Alert {
  id: number;
  machine_id: number;
  machine_code: string;
  machine_name: string;
  severity: AlertSeverity;
  status: AlertStatus;
  title: string;
  message: string;
  detected_at: string;
  acknowledged_at: string | null;
  acknowledged_by_id: number | null;
  resolved_at: string | null;
}

export interface StatusCount {
  status: MachineStatus;
  count: number;
}

export interface DashboardSummary {
  total_machines: number;
  operational_machines: number;
  active_alerts: number;
  average_efficiency: number;
  average_output_rate: number;
  status_counts: StatusCount[];
  recent_alerts: Alert[];
}

export interface ApiErrorResponse {
  error?: {
    code: string;
    message: string;
  };
}
