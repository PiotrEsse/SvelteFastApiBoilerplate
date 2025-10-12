<script lang="ts">
  import type { TodoStatus } from '$lib/api/sdk';

  export let status: TodoStatus;

  const label: Record<TodoStatus, string> = {
    pending: 'Do zrobienia',
    in_progress: 'W trakcie',
    completed: 'Ukończone'
  };

  const variants: Record<TodoStatus, string> = {
    pending: 'bg-amber-100 text-amber-800 border border-amber-200',
    in_progress: 'bg-sky-100 text-sky-800 border border-sky-200',
    completed: 'bg-emerald-100 text-emerald-800 border border-emerald-200'
  };
</script>

<span class={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${variants[status]}`}>
  {label[status]}
</span>
