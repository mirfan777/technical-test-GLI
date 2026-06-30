export type TaskStatus = 'Todo' | 'In Progress' | 'Done';

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: TaskStatus;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
}
