<script lang="ts">
  export let form:
    | {
        errors?: Record<string, string[]>;
        values?: Record<string, string>;
        message?: string;
      }
    | null;
</script>

<section class="mx-auto max-w-2xl rounded-2xl bg-white p-8 shadow">
  <h1 class="mb-2 text-2xl font-semibold text-slate-900">Utwórz konto</h1>
  <p class="mb-6 text-sm text-slate-600">
    Zarejestruj się, aby tworzyć, filtrować i aktualizować swoje zadania.
  </p>

  {#if form?.message}
    <div class="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
      {form.message}
    </div>
  {/if}

  <form method="POST" class="grid grid-cols-1 gap-5 md:grid-cols-2">
    <div class="md:col-span-2">
      <label for="fullName" class="mb-2 block text-sm font-medium text-slate-700">Imię i nazwisko</label>
      <input
        class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
        id="fullName"
        name="fullName"
        value={form?.values?.fullName ?? ''}
        required
      />
      {#if form?.errors?.fullName}
        <p class="mt-2 text-xs text-red-600">{form.errors.fullName[0]}</p>
      {/if}
    </div>

    <div class="md:col-span-2">
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
        autocomplete="new-password"
        required
      />
      {#if form?.errors?.password}
        <p class="mt-2 text-xs text-red-600">{form.errors.password[0]}</p>
      {/if}
    </div>

    <div>
      <label for="confirmPassword" class="mb-2 block text-sm font-medium text-slate-700"
        >Potwierdź hasło</label
      >
      <input
        class="block w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:ring-slate-500"
        id="confirmPassword"
        name="confirmPassword"
        type="password"
        autocomplete="new-password"
        required
      />
      {#if form?.errors?.confirmPassword}
        <p class="mt-2 text-xs text-red-600">{form.errors.confirmPassword[0]}</p>
      {/if}
    </div>

    <div class="md:col-span-2">
      <button
        type="submit"
        class="w-full rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-slate-700"
      >
        Zarejestruj się
      </button>
    </div>
  </form>

  <p class="mt-6 text-center text-xs text-slate-500">
    Masz już konto?
    <a class="font-medium text-slate-900" href="/login">Zaloguj się</a>.
  </p>
</section>
