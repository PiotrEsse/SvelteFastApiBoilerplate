import type { PageServerLoad } from './$types';
import { z } from 'zod';

const statusValues = ['pending', 'in_progress', 'completed'] as const;

const filtersSchema = z.object({
  search: z.string().optional(),
  status: z.enum(statusValues).optional()
});

export const load: PageServerLoad = async ({ locals, url }) => {
  const candidate = {
    search: url.searchParams.get('search') ?? undefined,
    status: url.searchParams.get('status') ?? undefined
  };

  const parsed = filtersSchema.safeParse(candidate);

  const filters = parsed.success ? parsed.data : {};

  const response = await locals.api.todos.list(filters);

  return {
    filters,
    initialTodos: response.items,
    total: response.total
  };
};
