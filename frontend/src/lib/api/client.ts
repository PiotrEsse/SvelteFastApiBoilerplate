import { browser } from '$app/environment';
import { PUBLIC_API_URL } from '$env/static/public';
import { createSdk, type TodoClient } from './sdk';

export interface CreateTodoClientOptions {
  fetch?: typeof fetch;
  accessToken?: string | null;
  baseUrl?: string;
}

const fallbackBaseUrl = () => {
  if (PUBLIC_API_URL) return PUBLIC_API_URL;
  return browser ? '' : 'http://localhost:8000';
};

export const createTodoClient = (options: CreateTodoClientOptions = {}): TodoClient => {
  const baseUrl = options.baseUrl ?? fallbackBaseUrl();
  const fetchImpl = options.fetch ?? fetch;
  const accessToken = options.accessToken ?? undefined;

  const wrappedFetch: typeof fetch = (input, init = {}) => {
    const requestInit: RequestInit = {
      ...init,
      credentials: 'include'
    };

    const headers = new Headers(init.headers ?? {});

    if (accessToken && !headers.has('Authorization')) {
      headers.set('Authorization', `Bearer ${accessToken}`);
    }

    requestInit.headers = headers;

    return fetchImpl(input, requestInit);
  };

  return createSdk({
    baseUrl,
    fetch: wrappedFetch
  });
};

export type { TodoClient } from './sdk';
