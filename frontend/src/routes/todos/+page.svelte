<script lang="ts">
  import { page } from '$app/stores';
  import { createQuery } from '@tanstack/svelte-query';
  import { createTodoClient } from '$lib/api/client';
  import TodoCard from '$lib/components/TodoCard.svelte';
  import type { TodoStatus } from '$lib/api/sdk';

  export let data: {
    filters: { search?: string; status?: TodoStatus };
    initialTodos: import('$lib/api/sdk').Todo[];
    total: number;
  };

  const client = createTodoClient();

  const parseStatus = (value: string | null): TodoStatus | undefined => {
    if (value === 'pending' || value === 'in_progress' || value === 'completed') {
      return value;
    }
    return undefined;
  };

  const todosQuery = createQuery(() => {
    const searchParams = $page.url.searchParams;
    const status = parseStatus(searchParams.get('status'));
    const search = searchParams.get('search') ?? undefined;

    return {
      queryKey: ['todos', { status, search }],
      queryFn: async () => {
        const response = await client.todos.list({ status, search });
        return response;
      },
      initialData: {
        items: data.initialTodos,
        total: data.total
      },
      staleTime: 1000 * 30
    };
  });

  const statusOptions: { value: TodoStatus | ''; label: string }[] = [
    { value: '', label: 'Wszystkie statusy' },
    { value: 'pending', label: 'Do zrobienia' },
    { value: 'in_progress', label: 'W trakcie' },
    { value: 'completed', label: 'Ukończone' }
  ];
</script>

<section class="space-y-8">
  <header class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
    <div>
      <h1 class="text-3xl font-semibold text-slate-900">Twoje zadania</h1>
      <p class="text-sm text-slate-600">Zarządzaj listą zadań i śledź postępy.</p>
    </div>
    <a
      href="/todos/new"
      class="inline-flex items-center justify-center rounded-lg bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow transition hover:bg-slate-700"
    >
      Dodaj zadanie
    </a>
  </header>

  <form method="GET" class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
    <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
      <div class="md:col-span-2">
        <label for="search" class="mb-2 block text-sm font-medium text-slate-700">Szukaj</label>
        <input
          id="search"
          name="search"
          value={data.filters.search ?? ''}
          placeholder="Nazwa, opis..."
          class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
        />
      </div>

      <div>
        <label for="status" class="mb-2 block text-sm font-medium text-slate-700">Status</label>
        <select
          id="status"
          name="status"
          class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
        >
          {#each statusOptions as option}
            <option value={option.value} selected={option.value === (data.filters.status ?? '')}>
              {option.label}
            </option>
          {/each}
        </select>
      </div>
    </div>

    <div class="mt-5 flex items-center justify-end gap-3">
      <a
        href="/todos"
        class="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:border-slate-300 hover:text-slate-900"
      >
        Wyczyść
      </a>
      <button
        type="submit"
        class="rounded-lg bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow transition hover:bg-slate-700"
      >
        Filtruj
      </button>
    </div>
  </form>

  {#if $todosQuery.isLoading}
    <p class="text-sm text-slate-600">Ładowanie zadań...</p>
  {:else if $todosQuery.isError}
    <p class="text-sm text-red-600">Nie udało się pobrać zadań. Spróbuj ponownie.</p>
  {:else if $todosQuery.data?.items.length}
    <div class="space-y-4">
      <p class="text-xs font-medium uppercase tracking-wide text-slate-500">
        Łącznie {$todosQuery.data.total} zadań
      </p>
      <div class="grid gap-4 md:grid-cols-2">
        {#each $todosQuery.data.items as todo}
          <TodoCard {todo} />
        {/each}
      </div>
    </div>
  {:else}
    <div class="rounded-2xl border border-dashed border-slate-200 bg-white p-10 text-center text-sm text-slate-500">
      Brak zadań spełniających kryteria.
    </div>
  {/if}
</section>
