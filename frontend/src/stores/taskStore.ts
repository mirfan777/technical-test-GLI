import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Task, TaskCreate, TaskStatus, TaskUpdate } from '../types/task';
import { taskService } from '../services/taskService';

export const useTaskStore = defineStore('tasks', () => {
  // State
  const tasks = ref<Task[]>([]);
  const isLoading = ref(false);
  const errorMsg = ref<string | null>(null);
  const successMsg = ref<string | null>(null);

  // Helper to trigger messages
  const triggerToast = (type: 'success' | 'error', message: string) => {
    if (type === 'success') {
      successMsg.value = message;
      setTimeout(() => {
        successMsg.value = null;
      }, 3000);
    } else {
      errorMsg.value = message;
      setTimeout(() => {
        errorMsg.value = null;
      }, 4000);
    }
  };

  // Actions
  const fetchTasks = async () => {
    isLoading.value = true;
    errorMsg.value = null;
    try {
      tasks.value = await taskService.getTasks();
    } catch (err: any) {
      triggerToast('error', 'Gagal memuat daftar task dari server.');
    } finally {
      isLoading.value = false;
    }
  };

  const createTask = async (taskData: TaskCreate) => {
    isLoading.value = true;
    try {
      const newTask = await taskService.createTask(taskData);
      tasks.value.push(newTask);
      triggerToast('success', 'Task baru berhasil ditambahkan.');
      return newTask;
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Gagal menyimpan task baru.';
      triggerToast('error', msg);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateTask = async (id: number, taskData: TaskUpdate) => {
    isLoading.value = true;
    try {
      const updated = await taskService.updateTask(id, taskData);
      const index = tasks.value.findIndex((t) => t.id === id);
      if (index !== -1) {
        tasks.value[index] = updated;
      }
      triggerToast('success', 'Task berhasil diperbarui.');
      return updated;
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Gagal memperbarui task.';
      triggerToast('error', msg);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateTaskStatus = async (id: number, newStatus: TaskStatus) => {
    try {
      const updated = await taskService.updateTask(id, { status: newStatus });
      const task = tasks.value.find((t) => t.id === id);
      if (task) {
        task.status = updated.status;
      }
      triggerToast('success', `Status task diubah menjadi "${newStatus}".`);
    } catch (err: any) {
      triggerToast('error', 'Gagal memperbarui status task.');
      throw err;
    }
  };

  const deleteTask = async (id: number) => {
    try {
      await taskService.deleteTask(id);
      tasks.value = tasks.value.filter((t) => t.id !== id);
      triggerToast('success', 'Task berhasil dihapus.');
    } catch (err: any) {
      triggerToast('error', 'Gagal menghapus task.');
      throw err;
    }
  };

  return {
    tasks,
    isLoading,
    errorMsg,
    successMsg,
    fetchTasks,
    createTask,
    updateTask,
    updateTaskStatus,
    deleteTask,
    triggerToast,
  };
});
