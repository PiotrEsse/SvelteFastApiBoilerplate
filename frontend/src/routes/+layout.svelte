<script lang="ts">
  import '$lib/styles/global.css';
  import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
  import { page } from '$app/stores';
  import { derived } from 'svelte/store';

  const queryClient = new QueryClient();
  const isAuthenticated = derived(page, ($page) => Boolean($page.data.accessToken));
</script>

<QueryClientProvider client={queryClient}>
  <div class="min-h-screen bg-gray-50">
    <header class="border-b bg-white/80 backdrop-blur">
      <nav class="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
        <a href="/" class="text-lg font-semibold text-slate-900">Todo App</a>
        <div class="flex items-center gap-4 text-sm font-medium">
          <a class="text-slate-600 transition hover:text-slate-900" href="/todos">Todos</a>
          {#if $isAuthenticated}
            <a class="text-slate-600 transition hover:text-slate-900" href="/todos/new">New Todo</a>
            <form method="POST" action="/logout" class="inline">
              <button
                type="submit"
                class="rounded-lg bg-slate-900 px-4 py-2 text-white transition hover:bg-slate-700"
              >
                Logout
              </button>
            </form>
          {:else}
            <a class="text-slate-600 transition hover:text-slate-900" href="/login">Log in</a>
            <a
              class="rounded-lg bg-slate-900 px-4 py-2 text-white transition hover:bg-slate-700"
              href="/register"
            >
              Sign up
            </a>
          {/if}
        </div>
      </nav>
    </header>

    <main class="mx-auto max-w-5xl px-4 py-8">
      <slot />
    </main>
  </div>
</QueryClientProvider>
