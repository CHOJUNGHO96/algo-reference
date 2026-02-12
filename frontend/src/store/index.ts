import { configureStore } from '@reduxjs/toolkit';
import { algorithmApi } from './api/algorithmApi';

export const store = configureStore({
  reducer: {
    [algorithmApi.reducerPath]: algorithmApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(algorithmApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
