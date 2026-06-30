<script setup lang="ts">
import type { Task, TaskStatus } from '../types/task';

defineProps<{
  task: Task;
}>();

const emit = defineEmits<{
  (e: 'update-status', id: number, newStatus: TaskStatus): void;
  (e: 'delete', id: number): void;
  (e: 'edit', task: Task): void;
}>();

const statuses: TaskStatus[] = ['Todo', 'In Progress', 'Done'];
</script>

<template>
  <div 
    class="group bg-white rounded-xl p-4 shadow-sm border border-slate-200/80 transition-all duration-200 flex flex-col gap-3 relative overflow-hidden hover:-translate-y-0.5 hover:shadow-md"
    :class="{
      'before:content-[\'\'] before:absolute before:top-0 before:left-0 before:w-1 before:h-full before:bg-amber-500 hover:border-amber-200/80': task.status === 'Todo',
      'before:content-[\'\'] before:absolute before:top-0 before:left-0 before:w-1 before:h-full before:bg-blue-500 hover:border-blue-200/80': task.status === 'In Progress',
      'before:content-[\'\'] before:absolute before:top-0 before:left-0 before:w-1 before:h-full before:bg-emerald-500 hover:border-emerald-200/80': task.status === 'Done'
    }"
  >
    <div class="flex justify-between items-start gap-3">
      <h3 class="m-0 text-base font-semibold text-slate-800 leading-snug break-words flex-grow">{{ task.title }}</h3>
      <div class="flex gap-1 opacity-40 group-hover:opacity-100 transition-opacity duration-200">
        <button class="bg-transparent border-none p-1.5 rounded-lg cursor-pointer text-slate-500 flex items-center justify-center transition-all duration-200 hover:bg-slate-100 hover:text-blue-500" @click="emit('edit', task)" title="Edit Task">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
          </svg>
        </button>
        <button class="bg-transparent border-none p-1.5 rounded-lg cursor-pointer text-slate-500 flex items-center justify-center transition-all duration-200 hover:bg-red-50 hover:text-red-500" @click="emit('delete', task.id)" title="Delete Task">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
          </svg>
        </button>
      </div>
    </div>
    
    <p class="m-0 text-sm text-slate-600 leading-relaxed line-clamp-3 break-words" v-if="task.description">{{ task.description }}</p>
    <p class="m-0 text-sm text-slate-400 italic" v-else>No description provided.</p>
    
    <div class="mt-auto pt-3 border-t border-dashed border-slate-100 flex justify-between items-center">
      <div class="flex items-center gap-2 w-full">
        <label class="text-[0.725rem] font-bold text-slate-400 uppercase tracking-wider">Status</label>
        <select 
          :value="task.status" 
          @change="(e) => emit('update-status', task.id, (e.target as HTMLSelectElement).value as TaskStatus)"
          class="flex-grow px-2 py-1.5 rounded-lg border border-slate-200 bg-white text-slate-700 text-xs font-semibold cursor-pointer outline-none transition-all duration-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        >
          <option v-for="status in statuses" :key="status" :value="status">
            {{ status }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>
