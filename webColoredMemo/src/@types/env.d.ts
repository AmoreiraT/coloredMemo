/// <reference types="vite/client.d.ts" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_AMBIENTE: string;
  readonly VITE_BASE_URL: string;

  readonly VITE_API_KEY: string;
  readonly VITE_AUTH_DOMAIN: string;
  readonly VITE_DATABASE_URL: string;
  readonly VITE_PROJECT_ID: string;
  readonly VITE_STORAGE_BUCKET: string;
  readonly VITE_MESSAGING_SENDER_ID: string;
  readonly VITE_APP_ID: string;
  readonly VITE_MEASUREMENT_ID: string;
  readonly VITE_APP_CHECK: string;

  readonly VITE_APP_ACCESS_CODE: string;
  readonly VITE_APP_USER_ID: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
