<script lang="ts">
  import TodoForm from '$lib/components/TodoForm.svelte';
  import StatusBadge from '$lib/components/StatusBadge.svelte';
  import type { Todo } from '$lib/api/sdk';

  export let data: { todo: Todo };
  export let form:
    | {
        errors?: Record<string, string[]>;
        values?: Record<string, string>;
        message?: string;
      }
    | null;

  const values = {
    title: form?.values?.title ?? data.todo.title,
    description: form?.values?.description ?? data.todo.description ?? '',
    status: form?.values?.status ?? data.todo.status,
    due_date: form?.values?.due_date ?? (data.todo.due_date ? data.todo.due_date.slice(0, 10) : '')
  };
</script>

<section class="mx-auto max-w-3xl space-y-6">
  <header class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
    <div class="flex items-start justify-between gap-4">
      <div>
        <h1 class="text-3xl font-semibold text-slate-900">{data.todo.title}</h1>
        <p class="text-sm text-slate-500">
          Utworzone {new Date(data.todo.created_at).toLocaleString()}
        </p>
      </div>
      <StatusBadge status={data.todo.status} />
    </div>
    {#if data.todo.description}
      <p class="text-sm text-slate-600">{data.todo.description}</p>
    {/if}
  </header>

  {#if form?.message}
    <div class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{form.message}</div>
  {/if}

  <form method="POST" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
    <TodoForm submitLabel="Zapisz zmiany" values={values} errors={form?.errors} />
  </form>

  <form method="POST" action="?/delete" class="flex justify-end">
    <button
      class="rounded-lg border border-red-200 bg-red-50 px-4 py-2 text-sm font-semibold text-red-700 transition hover:bg-red-100"
    >
      Usuń zadanie
    </button>
  </form>
</section>
