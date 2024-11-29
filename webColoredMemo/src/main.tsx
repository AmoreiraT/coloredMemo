// src/main.tsx
import React from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import './index.css';
import { queryClient } from './lib/queryClient';

// Removendo o React.StrictMode temporariamente para debug
ReactDOM.createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>
);