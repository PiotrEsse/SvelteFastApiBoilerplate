import { fail, redirect } from '@sveltejs/kit';
import { z } from 'zod';
import type { Actions, PageServerLoad } from './$types';
import { ApiError } from '$lib/api/sdk';
import { createTodoClient } from '$lib/api/client';

const registerSchema = z
  .object({
    email: z.string().email({ message: 'Podaj poprawny adres email.' }),
    password: z.string().min(8, { message: 'Hasło musi mieć co najmniej 8 znaków.' }),
    confirmPassword: z.string().min(8, { message: 'Potwierdź hasło.' }),
    fullName: z.string().min(1, { message: 'Imię i nazwisko jest wymagane.' })
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Hasła muszą być identyczne.',
    path: ['confirmPassword']
  });

export const load: PageServerLoad = async ({ locals }) => {
  if (locals.accessToken) {
    throw redirect(303, '/todos');
  }

  return {};
};

export const actions: Actions = {
  default: async ({ request, fetch }) => {
    const formData = await request.formData();
    const submission = {
      email: String(formData.get('email') ?? ''),
      password: String(formData.get('password') ?? ''),
      confirmPassword: String(formData.get('confirmPassword') ?? ''),
      fullName: String(formData.get('fullName') ?? '')
    };

    const parsed = registerSchema.safeParse(submission);

    if (!parsed.success) {
      const { fieldErrors } = parsed.error.flatten();
      return fail(400, {
        errors: fieldErrors,
        values: submission
      });
    }

    try {
      const api = createTodoClient({ fetch });
      await api.auth.register({
        email: parsed.data.email,
        password: parsed.data.password,
        full_name: parsed.data.fullName
      });

      throw redirect(303, '/login?registered=1');
    } catch (error) {
      if (error instanceof ApiError) {
        return fail(error.status, {
          message: error.body?.detail ?? 'Nie udało się utworzyć konta.',
          values: submission
        });
      }

      console.error('Unexpected registration error', error);
      return fail(500, {
        message: 'Wystąpił nieoczekiwany błąd.',
        values: submission
      });
    }
  }
};
