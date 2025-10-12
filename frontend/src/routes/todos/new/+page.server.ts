import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { todoFormSchema } from '$lib/validation/todo';
import { ApiError } from '$lib/api/sdk';
import { createTodoClient } from '$lib/api/client';

export const load: PageServerLoad = async ({ locals }) => {
  if (!locals.accessToken) {
    throw redirect(303, '/login');
  }

  return {
    initialValues: {
      status: 'pending'
    }
  };
};

export const actions: Actions = {
  default: async ({ request, fetch }) => {
    const formData = await request.formData();
    const candidate = {
      title: formData.get('title'),
      description: formData.get('description'),
      status: formData.get('status') ?? 'pending',
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
          status: String(candidate.status ?? 'pending'),
          due_date: String(candidate.due_date ?? '')
        }
      });
    }

    try {
      const api = createTodoClient({ fetch });
      await api.todos.create({
        title: parsed.data.title,
        description: parsed.data.description ?? undefined,
        status: parsed.data.status,
        due_date: parsed.data.due_date ?? undefined
      });

      throw redirect(303, '/todos');
    } catch (error) {
      if (error instanceof ApiError) {
        return fail(error.status, {
          message: error.body?.detail ?? 'Nie udało się utworzyć zadania.',
          values: {
            title: parsed.data.title,
            description: parsed.data.description ?? '',
            status: parsed.data.status,
            due_date: parsed.data.due_date ?? ''
          }
        });
      }

      console.error('Unexpected todo create error', error);
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
  }
};
