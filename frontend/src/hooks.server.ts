import type { Handle } from '@sveltejs/kit';
import { createTodoClient } from '$lib/api/client';

export const handle: Handle = async ({ event, resolve }) => {
  const accessToken = event.cookies.get('access_token') ?? undefined;

  const originalFetch = event.fetch;
  event.fetch = async (input, init = {}) => {
    const headers = new Headers(init.headers ?? {});

    if (accessToken && !headers.has('Authorization')) {
      headers.set('Authorization', `Bearer ${accessToken}`);
    }

    const nextInit: RequestInit = {
      ...init,
      credentials: 'include',
      headers
    };

    return originalFetch(input, nextInit);
  };

  event.locals.accessToken = accessToken;
  event.locals.api = createTodoClient({
    accessToken,
    fetch: event.fetch
  });

  const response = await resolve(event);

  return response;
};
