import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ locals, cookies }) => {
  try {
    await locals.api.auth.logout();
  } catch (error) {
    // Swallow logout errors – the session will be cleared either way.
    console.error('Failed to revoke session', error);
  }

  cookies.delete('access_token', { path: '/' });

  throw redirect(303, '/login');
};
