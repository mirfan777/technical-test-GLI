<script setup lang="ts">
import type { Task, TaskStatus } from '../types/task';
import TaskCard from './TaskCard.vue';

const props = defineProps<{
  title: TaskStatus;
  tasks: Task[];
}>();

const emit = defineEmits<{
  (e: 'update-status', id: number, newStatus: TaskStatus): void;
  (e: 'delete', id: number): void;
  (e: 'edit', task: Task): void;
  (e: 'add-task-click', status: TaskStatus): void;
}>();
</script>

<template>
  <div 
    class="flex-1 min-w-[280px] bg-slate-50/70 rounded-2xl p-4 flex flex-col gap-4 border border-slate-200/50"
  >
    <div class="flex justify-between items-center">
      <div class="flex items-center gap-2">
        <span 
          class="w-2.5 h-2.5 rounded-full"
          :class="{
            'bg-amber-500': title === 'Todo',
            'bg-blue-500': title === 'In Progress',
            'bg-emerald-500': title === 'Done'
          }"
        ></span>
        <h2 class="m-0 text-sm font-bold text-slate-800">{{ title }}</h2>
        <span 
          class="text-xs font-semibold px-2 py-0.5 rounded-full"
          :class="{
            'bg-amber-550/10 text-amber-700 bg-amber-50': title === 'Todo',
            'bg-blue-550/10 text-blue-700 bg-blue-50': title === 'In Progress',
            'bg-emerald-550/10 text-emerald-700 bg-emerald-50': title === 'Done'
          }"
        >
          {{ tasks.length }}
        </span>
      </div>
      
      <button 
        class="bg-transparent border-none p-1.5 rounded-lg cursor-pointer text-slate-400 flex items-center justify-center transition-all duration-200 hover:bg-slate-200/60 hover:text-slate-700" 
        @click="emit('add-task-click', title)"
        title="Add task to this column"
      >
        <svg viewBox="0 0 24 24" width="16" height="16">
          <path fill="currentColor" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
        </svg>
      </button>
    </div>
    
    <div class="flex flex-col gap-3 flex-grow overflow-y-auto min-h-[200px]">
      <template v-if="tasks.length > 0">
        <TaskCard 
          v-for="task in tasks" 
          :key="task.id" 
          :task="task" 
          @update-status="(id, status) => emit('update-status', id, status)"
          @delete="(id) => emit('delete', id)"
          @edit="(task) => emit('edit', task)"
        />
      </template>
      <div class="flex flex-col items-center justify-center gap-2 py-8 px-4 text-slate-400/80 text-xs border border-dashed border-slate-200 rounded-xl bg-white/30 flex-grow min-h-[150px]" v-else>
        <svg viewBox="0 0 24 24" width="24" height="24" class="opacity-20">
          <path fill="currentColor" d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
        </svg>
        <span>No tasks in this column</span>
      </div>
    </div>
  </div>
</template>
