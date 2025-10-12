export type TodoStatus = 'pending' | 'in_progress' | 'completed';

export interface Todo {
  id: string;
  title: string;
  description?: string | null;
  status: TodoStatus;
  due_date?: string | null;
  created_at: string;
  updated_at: string;
}

export interface TodoListResponse {
  items: Todo[];
  total: number;
}

export interface DueSoonQuery {
  hours?: number;
}

export interface TriggerRemindersResponse {
  task_id: string;
}

export interface TodoFilters {
  search?: string;
  status?: TodoStatus;
  page?: number;
  page_size?: number;
}

export interface CreateTodoInput {
  title: string;
  description?: string | null;
  status?: TodoStatus;
  due_date?: string | null;
}

export interface UpdateTodoInput {
  title?: string;
  description?: string | null;
  status?: TodoStatus;
  due_date?: string | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface ApiErrorDetails {
  detail?: string;
  errors?: Record<string, string[]>;
}

export class ApiError extends Error {
  status: number;
  body: ApiErrorDetails | undefined;

  constructor(status: number, message: string, body?: ApiErrorDetails) {
    super(message);
    this.status = status;
    this.body = body;
  }
}

export interface SdkConfig {
  baseUrl: string;
  fetch: typeof fetch;
}

type Query = Record<string, string | number | boolean | undefined | null>;

const buildQuery = (query?: Query) => {
  if (!query) return '';
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === '') continue;
    params.set(key, String(value));
  }
  const qs = params.toString();
  return qs ? `?${qs}` : '';
};

export const createSdk = (config: SdkConfig) => {
  const request = async <T>(path: string, init: RequestInit = {}, query?: Query): Promise<T> => {
    const url = `${config.baseUrl}${path}${buildQuery(query)}`;
    const headers = new Headers(init.headers ?? {});
    const hasBody = init.body !== undefined && !(init.body instanceof FormData);
    if (hasBody && !headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json');
    }

    const response = await config.fetch(url, { ...init, headers });

    const contentType = response.headers.get('content-type') ?? '';
    const isJson = contentType.includes('application/json');
    const data = isJson ? await response.json() : undefined;

    if (!response.ok) {
      throw new ApiError(response.status, response.statusText, data);
    }

    return data as T;
  };

  return {
    auth: {
      login: (payload: LoginRequest) =>
        request<LoginResponse>('/auth/login', {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      register: (payload: RegisterRequest) =>
        request<void>('/auth/register', {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      logout: () =>
        request<void>('/auth/logout', {
          method: 'POST'
        })
    },
    todos: {
      list: (filters?: TodoFilters) =>
        request<TodoListResponse>('/todos', { method: 'GET' }, filters),
      get: (id: string) => request<Todo>(`/todos/${id}`, { method: 'GET' }),
      dueSoon: (query?: DueSoonQuery) =>
        request<Todo[]>(`/todos/due-soon`, { method: 'GET' }, query),
      triggerReminders: () =>
        request<TriggerRemindersResponse>(`/todos/trigger-reminders`, {
          method: 'POST'
        }),
      create: (payload: CreateTodoInput) =>
        request<Todo>('/todos', {
          method: 'POST',
          body: JSON.stringify(payload)
        }),
      update: (id: string, payload: UpdateTodoInput) =>
        request<Todo>(`/todos/${id}`, {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }),
      remove: (id: string) =>
        request<void>(`/todos/${id}`, {
          method: 'DELETE'
        })
    }
  };
};

export type TodoClient = ReturnType<typeof createSdk>;
