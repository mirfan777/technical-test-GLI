<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { storeToRefs } from 'pinia';
import type { Task, TaskStatus } from '../types/task';
import { useTaskStore } from '../stores/taskStore';
import KanbanColumn from './KanbanColumn.vue';

// Use Pinia Store
const taskStore = useTaskStore();
const { tasks, isLoading, errorMsg, successMsg } = storeToRefs(taskStore);

// Local UI States
const isModalOpen = ref(false);
const isEditing = ref(false);
const editingTaskId = ref<number | null>(null);

const formTitle = ref('');
const formDescription = ref('');
const formStatus = ref<TaskStatus>('Todo');
const formError = ref<string | null>(null);

// Columns definitions
const columns: TaskStatus[] = ['Todo', 'In Progress', 'Done'];

// Columns grouping
const todoTasks = computed(() => tasks.value.filter((t) => t.status === 'Todo'));
const inProgressTasks = computed(() => tasks.value.filter((t) => t.status === 'In Progress'));
const doneTasks = computed(() => tasks.value.filter((t) => t.status === 'Done'));

// Methods
const openCreateModal = (defaultStatus: TaskStatus = 'Todo') => {
  isEditing.value = false;
  editingTaskId.value = null;
  formTitle.value = '';
  formDescription.value = '';
  formStatus.value = defaultStatus;
  formError.value = null;
  isModalOpen.value = true;
};

const openEditModal = (task: Task) => {
  isEditing.value = true;
  editingTaskId.value = task.id;
  formTitle.value = task.title;
  formDescription.value = task.description || '';
  formStatus.value = task.status;
  formError.value = null;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  formError.value = null;
};

const handleSubmit = async () => {
  if (!formTitle.value.trim()) {
    formError.value = 'Judul task tidak boleh kosong';
    return;
  }
  
  formError.value = null;
  
  try {
    if (isEditing.value && editingTaskId.value !== null) {
      await taskStore.updateTask(editingTaskId.value, {
        title: formTitle.value.trim(),
        description: formDescription.value.trim() || undefined,
        status: formStatus.value,
      });
    } else {
      await taskStore.createTask({
        title: formTitle.value.trim(),
        description: formDescription.value.trim() || undefined,
        status: formStatus.value,
      });
    }
    closeModal();
  } catch (err: any) {
    formError.value = err.response?.data?.detail || 'Gagal menyimpan task. Coba lagi.';
  }
};

const handleUpdateStatus = async (id: number, newStatus: TaskStatus) => {
  try {
    await taskStore.updateTaskStatus(id, newStatus);
  } catch (err: any) {
    // Error is handled inside store with triggerToast
  }
};

const handleDeleteTask = async (id: number) => {
  if (!confirm('Apakah Anda yakin ingin menghapus task ini?')) return;
  try {
    await taskStore.deleteTask(id);
  } catch (err: any) {
    // Error is handled inside store with triggerToast
  }
};

onMounted(() => {
  taskStore.fetchTasks();
});
</script>

<template>
  <div class="max-w-[1200px] mx-auto px-6 py-8 flex flex-col gap-8 min-h-[80vh]">
    <!-- Header -->
    <header class="flex justify-between items-center flex-wrap gap-4 pb-6 border-b border-slate-200/80">
      <div class="flex items-center gap-3">
        <button class="bg-gradient-to-br from-blue-500 to-blue-600 text-white border-none px-4 py-2 rounded-xl text-sm font-semibold cursor-pointer flex items-center gap-1.5 shadow-md shadow-blue-500/20 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-blue-500/30 active:translate-y-0" @click="openCreateModal('Todo')">
          <svg viewBox="0 0 24 24" width="18" height="18">
            <path fill="currentColor" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
          </svg>
          Tambah Task
        </button>
      </div>
    </header>

    <!-- Alert / Toast Message -->
    <Transition 
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-6 scale-90"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 -translate-y-6 scale-90"
    >
      <div class="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl text-white text-sm font-semibold flex items-center gap-2.5 shadow-xl max-w-[350px] bg-emerald-500" v-if="successMsg">
        <svg viewBox="0 0 24 24" width="18" height="18">
          <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
        </svg>
        <span>{{ successMsg }}</span>
      </div>
    </Transition>
    
    <Transition 
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-6 scale-90"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 -translate-y-6 scale-90"
    >
      <div class="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl text-white text-sm font-semibold flex items-center gap-2.5 shadow-xl max-w-[350px] bg-red-500" v-if="errorMsg">
        <svg viewBox="0 0 24 24" width="18" height="18">
          <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
        </svg>
        <span>{{ errorMsg }}</span>
      </div>
    </Transition>

    <!-- Loading Indicator -->
    <div class="flex flex-col items-center justify-center py-16 text-slate-500 gap-3" v-if="isLoading && tasks.length === 0">
      <div class="w-10 h-10 border-4 border-slate-200 border-t-blue-500 rounded-full animate-spin"></div>
      <p class="text-sm font-medium text-slate-400">Memuat data task...</p>
    </div>

    <!-- Kanban Board Grid -->
    <main class="flex gap-5 overflow-x-auto pb-4 items-start" v-else>
      <KanbanColumn 
        title="Todo" 
        :tasks="todoTasks"
        @update-status="handleUpdateStatus"
        @delete="handleDeleteTask"
        @edit="openEditModal"
        @add-task-click="openCreateModal"
      />
      <KanbanColumn 
        title="In Progress" 
        :tasks="inProgressTasks"
        @update-status="handleUpdateStatus"
        @delete="handleDeleteTask"
        @edit="openEditModal"
        @add-task-click="openCreateModal"
      />
      <KanbanColumn 
        title="Done" 
        :tasks="doneTasks"
        @update-status="handleUpdateStatus"
        @delete="handleDeleteTask"
        @edit="openEditModal"
        @add-task-click="openCreateModal"
      />
    </main>

    <!-- Form / Modal Dialog -->
    <Transition 
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-[2px] flex items-center justify-center z-50 p-4" v-if="isModalOpen" @click.self="closeModal">
        <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl border border-slate-200/60 overflow-hidden flex flex-col transform transition-all duration-200 scale-100">
          <div class="px-5 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <h2 class="m-0 text-base font-bold text-slate-800">{{ isEditing ? 'Edit Tugas' : 'Tambah Tugas Baru' }}</h2>
            <button class="bg-transparent border-none cursor-pointer text-slate-400 p-1.5 rounded-lg flex items-center justify-center transition-all duration-200 hover:bg-slate-200/60 hover:text-slate-800" @click="closeModal">
              <svg viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="handleSubmit" class="p-5 flex flex-col gap-4">
            <div class="flex flex-col gap-1.5">
              <label for="title" class="text-xs font-bold text-slate-400 uppercase tracking-wider">Judul Tugas <span class="text-red-500">*</span></label>
              <input 
                type="text" 
                id="title" 
                v-model="formTitle" 
                placeholder="Masukkan judul tugas..." 
                class="px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-700 text-sm outline-none transition-all duration-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                required
                autocomplete="off"
              />
            </div>
            
            <div class="flex flex-col gap-1.5">
              <label for="description" class="text-xs font-bold text-slate-400 uppercase tracking-wider">Deskripsi</label>
              <textarea 
                id="description" 
                v-model="formDescription" 
                placeholder="Masukkan deskripsi tugas (opsional)..." 
                class="px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-700 text-sm outline-none transition-all duration-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 resize-none"
                rows="4"
              ></textarea>
            </div>
            
            <div class="flex flex-col gap-1.5">
              <label for="status" class="text-xs font-bold text-slate-400 uppercase tracking-wider">Status</label>
              <select id="status" v-model="formStatus" class="px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-700 text-sm outline-none transition-all duration-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 cursor-pointer">
                <option v-for="status in columns" :key="status" :value="status">
                  {{ status }}
                </option>
              </select>
            </div>
            
            <div class="text-red-500 text-xs font-medium" v-if="formError">{{ formError }}</div>
            
            <div class="flex justify-end gap-2.5 mt-2 pt-4 border-t border-slate-100">
              <button type="button" class="px-4 py-2.5 rounded-xl text-sm font-semibold cursor-pointer transition-all duration-200 bg-slate-100 text-slate-600 border border-slate-200/60 hover:bg-slate-200" @click="closeModal" :disabled="isLoading">Batal</button>
              <button type="submit" class="px-4 py-2.5 rounded-xl text-sm font-semibold cursor-pointer transition-all duration-200 bg-blue-500 text-white border-none hover:bg-blue-600" :disabled="isLoading">
                <span>{{ isEditing ? 'Simpan' : 'Tambah' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>
