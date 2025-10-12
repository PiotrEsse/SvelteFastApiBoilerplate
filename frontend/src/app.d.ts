// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import type { TodoClient } from '$lib/api/client';

declare global {
  namespace App {
    interface Locals {
      api: TodoClient;
      accessToken?: string;
    }

    interface PageData {
      accessToken?: string;
      registered?: boolean;
    }
  }
}

export {};
