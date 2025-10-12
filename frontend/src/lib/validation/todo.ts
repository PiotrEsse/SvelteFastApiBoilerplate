import { z } from 'zod';

const statusValues = ['pending', 'in_progress', 'completed'] as const;

type MaybeString = FormDataEntryValue | null | undefined;

const emptyToUndefined = (value: MaybeString) => {
  if (typeof value !== 'string') return undefined;
  const trimmed = value.trim();
  return trimmed.length ? trimmed : undefined;
};

export const todoFormSchema = z.object({
  title: z.string().min(1, { message: 'Tytuł jest wymagany.' }),
  description: z
    .preprocess(
      (value) => emptyToUndefined(value) ?? null,
      z.string().max(1000, { message: 'Opis może mieć maksymalnie 1000 znaków.' }).nullable()
    )
    .optional(),
  status: z.enum(statusValues).default('pending'),
  due_date: z
    .preprocess(
      (value) => emptyToUndefined(value) ?? null,
      z
        .string()
        .regex(/^\d{4}-\d{2}-\d{2}$/, { message: 'Użyj formatu RRRR-MM-DD.' })
        .nullable()
    )
    .optional()
});

export type TodoFormInput = z.infer<typeof todoFormSchema>;
