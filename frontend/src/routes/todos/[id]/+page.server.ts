import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { todoFormSchema } from '$lib/validation/todo';
import { ApiError } from '$lib/api/sdk';
import { createTodoClient } from '$lib/api/client';

export const load: PageServerLoad = async ({ locals, params }) => {
  if (!locals.accessToken) {
    throw redirect(303, '/login');
  }

  const todo = await locals.api.todos.get(params.id);

  return {
    todo
  };
};

export const actions: Actions = {
  default: async ({ request, fetch, params }) => {
    const formData = await request.formData();
    const candidate = {
      title: formData.get('title'),
      description: formData.get('description'),
      status: formData.get('status'),
      due_date: formData.get('due_date')
    };

    const parsed = todoFormSchema.safeParse(candidate);

    if (!parsed.success) {
      const { fieldErrors } = parsed.error.flatten();
      return fail(400, {
        errors: fieldErrors,
        values: {
          title: String(candidate.title ?? ''),
          description: String(candidate.description ?? ''),
          status: String(candidate.status ?? ''),
          due_date: String(candidate.due_date ?? '')
        }
      });
    }

    try {
      const api = createTodoClient({ fetch });
      await api.todos.update(params.id, {
        title: parsed.data.title,
        description: parsed.data.description ?? undefined,
        status: parsed.data.status,
        due_date: parsed.data.due_date ?? undefined
      });

      throw redirect(303, `/todos/${params.id}`);
    } catch (error) {
      if (error instanceof ApiError) {
        return fail(error.status, {
          message: error.body?.detail ?? 'Nie udało się zaktualizować zadania.',
          values: {
            title: parsed.data.title,
            description: parsed.data.description ?? '',
            status: parsed.data.status,
            due_date: parsed.data.due_date ?? ''
          }
        });
      }

      console.error('Unexpected todo update error', error);
      return fail(500, {
        message: 'Wystąpił nieoczekiwany błąd.',
        values: {
          title: parsed.data.title,
          description: parsed.data.description ?? '',
          status: parsed.data.status,
          due_date: parsed.data.due_date ?? ''
        }
      });
    }
  },
  delete: async ({ params, fetch }) => {
    try {
      const api = createTodoClient({ fetch });
      await api.todos.remove(params.id);
    } catch (error) {
      if (error instanceof ApiError) {
        return fail(error.status, {
          message: error.body?.detail ?? 'Nie udało się usunąć zadania.'
        });
      }

      console.error('Unexpected todo delete error', error);
      return fail(500, {
        message: 'Wystąpił nieoczekiwany błąd podczas usuwania zadania.'
      });
    }

    throw redirect(303, '/todos');
  }
};
