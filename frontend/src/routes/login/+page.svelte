<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;
  export let form: {
    errors?: Record<string, string[]>;
    values?: Record<string, string>;
    message?: string;
  } | null;
</script>

<section class="mx-auto max-w-md rounded-2xl bg-white p-8 shadow">
  <h1 class="mb-2 text-2xl font-semibold text-slate-900">Zaloguj się</h1>
  <p class="mb-6 text-sm text-slate-600">
    Uzyskaj dostęp do swojej listy zadań, logując się na konto.
  </p>

  {#if data.registered}
    <div class="mb-4 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
      Konto zostało utworzone. Możesz się teraz zalogować.
    </div>
  {/if}

  {#if form?.message}
    <div class="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
      {form.message}
    </div>
  {/if}

  <form method="POST" class="space-y-5">
    <div>
      <label for="email" class="mb-2 block text-sm font-medium text-slate-700">Email</label>
      <input
        class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
        id="email"
        name="email"
        type="email"
        value={form?.values?.email ?? ''}
        required
      />
      {#if form?.errors?.email}
        <p class="mt-2 text-xs text-red-600">{form.errors.email[0]}</p>
      {/if}
    </div>

    <div>
      <label for="password" class="mb-2 block text-sm font-medium text-slate-700">Hasło</label>
      <input
        class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
        id="password"
        name="password"
        type="password"
        autocomplete="current-password"
        required
      />
      {#if form?.errors?.password}
        <p class="mt-2 text-xs text-red-600">{form.errors.password[0]}</p>
      {/if}
    </div>

    <button
      type="submit"
      class="w-full rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-slate-700"
    >
      Zaloguj się
    </button>
  </form>

  <p class="mt-6 text-center text-xs text-slate-500">
    Nie masz konta?
    <a class="font-medium text-slate-900" href="/register">Zarejestruj się</a>.
  </p>
</section>
