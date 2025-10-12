<script lang="ts">
  import type { TodoStatus } from '$lib/api/sdk';

  export interface TodoFormValues {
    title?: string;
    description?: string | null;
    status?: TodoStatus;
    due_date?: string | null;
  }

  export let values: TodoFormValues = {};
  export let errors: Record<string, string[]> | undefined;
  export let submitLabel = 'Zapisz';

  const statuses: { value: TodoStatus; label: string }[] = [
    { value: 'pending', label: 'Do zrobienia' },
    { value: 'in_progress', label: 'W trakcie' },
    { value: 'completed', label: 'Ukończone' }
  ];
</script>

<div class="space-y-5">
  <div>
    <label for="title" class="mb-2 block text-sm font-medium text-slate-700">Tytuł</label>
    <input
      id="title"
      name="title"
      value={values.title ?? ''}
      required
      class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
    />
    {#if errors?.title}
      <p class="mt-2 text-xs text-red-600">{errors.title[0]}</p>
    {/if}
  </div>

  <div>
    <label for="description" class="mb-2 block text-sm font-medium text-slate-700">Opis</label>
    <textarea
      id="description"
      name="description"
      rows="4"
      class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
    >{values.description ?? ''}</textarea>
    {#if errors?.description}
      <p class="mt-2 text-xs text-red-600">{errors.description[0]}</p>
    {/if}
  </div>

  <div class="grid grid-cols-1 gap-5 md:grid-cols-2">
    <div>
      <label for="status" class="mb-2 block text-sm font-medium text-slate-700">Status</label>
      <select
        id="status"
        name="status"
        class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
      >
        {#each statuses as option}
          <option value={option.value} selected={values.status === option.value}>
            {option.label}
          </option>
        {/each}
      </select>
      {#if errors?.status}
        <p class="mt-2 text-xs text-red-600">{errors.status[0]}</p>
      {/if}
    </div>

    <div>
      <label for="due_date" class="mb-2 block text-sm font-medium text-slate-700">Termin</label>
      <input
        id="due_date"
        name="due_date"
        type="date"
        value={values.due_date ?? ''}
        class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
      />
      {#if errors?.due_date}
        <p class="mt-2 text-xs text-red-600">{errors.due_date[0]}</p>
      {/if}
    </div>
  </div>

  <div class="flex justify-end">
    <button
      type="submit"
      class="rounded-lg bg-slate-900 px-6 py-2 text-sm font-semibold text-white shadow transition hover:bg-slate-700"
    >
      {submitLabel}
    </button>
  </div>
</div>
