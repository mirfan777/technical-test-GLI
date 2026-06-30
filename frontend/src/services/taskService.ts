import axios from 'axios';
import type { Task, TaskCreate, TaskUpdate } from '../types/task';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const taskService = {
  async getTasks(): Promise<Task[]> {
    const response = await apiClient.get<Task[]>('/tasks/');
    return response.data;
  },

  async createTask(task: TaskCreate): Promise<Task> {
    const response = await apiClient.post<Task>('/tasks/', task);
    return response.data;
  },

  async updateTask(id: number, task: TaskUpdate): Promise<Task> {
    const response = await apiClient.patch<Task>(`/tasks/${id}`, task);
    return response.data;
  },

  async deleteTask(id: number): Promise<void> {
    await apiClient.delete(`/tasks/${id}`);
  },
};
