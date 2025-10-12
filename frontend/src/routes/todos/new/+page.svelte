<script lang="ts">
  import TodoForm from '$lib/components/TodoForm.svelte';
  import type { TodoStatus } from '$lib/api/sdk';

  export let data: { initialValues: { status: TodoStatus } };
  export let form:
    | {
        errors?: Record<string, string[]>;
        values?: Record<string, string>;
        message?: string;
      }
    | null;

  const values = {
    status: form?.values?.status ?? data.initialValues.status,
    title: form?.values?.title,
    description: form?.values?.description,
    due_date: form?.values?.due_date
  };
</script>

<section class="mx-auto max-w-3xl space-y-6">
  <header>
    <h1 class="text-3xl font-semibold text-slate-900">Nowe zadanie</h1>
    <p class="text-sm text-slate-600">Utwórz nowe zadanie i przypisz mu termin.</p>
  </header>

  {#if form?.message}
    <div class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{form.message}</div>
  {/if}

  <form method="POST" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
    <TodoForm submitLabel="Utwórz zadanie" values={values} errors={form?.errors} />
  </form>
</section>
