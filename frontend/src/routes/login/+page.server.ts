import { fail, redirect } from '@sveltejs/kit';
import { z } from 'zod';
import { dev } from '$app/environment';
import type { Actions, PageServerLoad } from './$types';
import { createTodoClient } from '$lib/api/client';
import { ApiError } from '$lib/api/sdk';

const loginSchema = z.object({
  email: z.string().email({ message: 'Podaj poprawny adres email.' }),
  password: z.string().min(1, { message: 'Hasło jest wymagane.' })
});

export const load: PageServerLoad = async ({ locals, url }) => {
  if (locals.accessToken) {
    throw redirect(303, '/todos');
  }

  const registered = url.searchParams.get('registered') === '1';

  return {
    registered
  };
};

export const actions: Actions = {
  default: async ({ request, cookies, fetch }) => {
    const formData = await request.formData();
    const submission = {
      email: String(formData.get('email') ?? ''),
      password: String(formData.get('password') ?? '')
    };

    const parsed = loginSchema.safeParse(submission);

    if (!parsed.success) {
      const { fieldErrors } = parsed.error.flatten();
      return fail(400, {
        errors: fieldErrors,
        values: submission
      });
    }

    try {
      const api = createTodoClient({ fetch });
      const response = await api.auth.login(parsed.data);

      cookies.set('access_token', response.access_token, {
        path: '/',
        httpOnly: true,
        sameSite: 'lax',
        secure: !dev,
        maxAge: 60 * 60 * 24 * 7
      });

      throw redirect(303, '/todos');
    } catch (error) {
      if (error instanceof ApiError) {
        return fail(error.status, {
          message: error.body?.detail ?? 'Nie udało się zalogować.',
          values: submission
        });
      }

      console.error('Unexpected login error', error);
      return fail(500, {
        message: 'Wystąpił nieoczekiwany błąd.',
        values: submission
      });
    }
  }
};
