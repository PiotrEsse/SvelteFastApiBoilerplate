<script lang="ts">
  import StatusBadge from '$lib/components/StatusBadge.svelte';
  import type { Todo } from '$lib/api/sdk';

  export let todo: Todo;
</script>

<article class="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
  <header class="flex items-start justify-between gap-4">
    <div>
      <h2 class="text-lg font-semibold text-slate-900">{todo.title}</h2>
      <p class="mt-1 text-sm text-slate-500">
        Ostatnia aktualizacja: {new Date(todo.updated_at).toLocaleString()}
      </p>
    </div>
    <StatusBadge status={todo.status} />
  </header>

  {#if todo.description}
    <p class="text-sm text-slate-700">{todo.description}</p>
  {/if}

  <footer class="flex items-center justify-between text-sm text-slate-500">
    {#if todo.due_date}
      <span>Termin: {new Date(todo.due_date).toLocaleDateString()}</span>
    {/if}
    <a class="text-slate-900 underline-offset-4 hover:underline" href={`/todos/${todo.id}`}>
      Edytuj
    </a>
  </footer>
</article>
