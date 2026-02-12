---
name: algo-reference-state
description: Redux Toolkit 상태 관리 패턴. Use when working with global state, Redux slices, or async actions.
---

# Algo Reference State Management

Redux Toolkit을 사용한 전역 상태 관리 패턴입니다.

## Store 설정

### store.ts

```typescript
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import userReducer from './userSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    user: userReducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false  // Date 객체 등 직렬화 불가능한 값 허용
    })
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Provider 설정

```typescript
// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './store';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
```

## Slice 작성

### Auth Slice

```typescript
// src/store/authSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { api } from '../services/api';

type User = {
  id: number;
  email: string;
  fullName: string;
};

type AuthState = {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
};

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  isLoading: false,
  error: null
};

// Async Thunks
export const login = createAsyncThunk(
  'auth/login',
  async (credentials: { email: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await api.post('/auth/login', credentials);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Login failed');
    }
  }
);

export const logout = createAsyncThunk('auth/logout', async () => {
  localStorage.removeItem('token');
});

export const fetchCurrentUser = createAsyncThunk(
  'auth/fetchCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch user');
    }
  }
);

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setToken: (state, action: PayloadAction<string>) => {
      state.token = action.payload;
      localStorage.setItem('token', action.payload);
    },
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.access_token;
        localStorage.setItem('token', action.payload.access_token);
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Logout
    builder.addCase(logout.fulfilled, (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
    });

    // Fetch Current User
    builder
      .addCase(fetchCurrentUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload;
      })
      .addCase(fetchCurrentUser.rejected, (state) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
        localStorage.removeItem('token');
      });
  }
});

export const { setToken, clearError } = authSlice.actions;
export default authSlice.reducer;
```

## Hooks 사용

### Custom Hooks

```typescript
// src/hooks/useAppDispatch.ts
import { useDispatch } from 'react-redux';
import type { AppDispatch } from '../store';

export const useAppDispatch = () => useDispatch<AppDispatch>();
```

```typescript
// src/hooks/useAppSelector.ts
import { useSelector } from 'react-redux';
import type { RootState } from '../store';

export const useAppSelector = <T>(selector: (state: RootState) => T): T => {
  return useSelector(selector);
};
```

### 컴포넌트에서 사용

```typescript
// src/pages/Login.tsx
import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks';
import { login, clearError } from '../store/authSlice';

export function LoginPage() {
  const dispatch = useAppDispatch();
  const { isLoading, error, isAuthenticated } = useAppSelector((state) => state.auth);

  const handleLogin = async (email: string, password: string) => {
    const result = await dispatch(login({ email, password }));

    if (login.fulfilled.match(result)) {
      // 로그인 성공
      navigate('/dashboard');
    }
  };

  useEffect(() => {
    return () => {
      dispatch(clearError());
    };
  }, [dispatch]);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" />;
  }

  return <LoginForm onSubmit={handleLogin} isLoading={isLoading} error={error} />;
}
```

## 고급 패턴

### RTK Query (API 캐싱)

```typescript
// src/services/api.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_BASE_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
      return headers;
    }
  }),
  tagTypes: ['User'],
  endpoints: (builder) => ({
    getUsers: builder.query<User[], void>({
      query: () => '/users',
      providesTags: ['User']
    }),
    getUser: builder.query<User, number>({
      query: (id) => `/users/${id}`,
      providesTags: (result, error, id) => [{ type: 'User', id }]
    }),
    createUser: builder.mutation<User, Partial<User>>({
      query: (user) => ({
        url: '/users',
        method: 'POST',
        body: user
      }),
      invalidatesTags: ['User']
    })
  })
});

export const { useGetUsersQuery, useGetUserQuery, useCreateUserMutation } = api;
```

### Slice Selector

```typescript
// src/store/authSlice.ts
export const selectIsAuthenticated = (state: RootState) => state.auth.isAuthenticated;
export const selectCurrentUser = (state: RootState) => state.auth.user;
export const selectAuthError = (state: RootState) => state.auth.error;

// 컴포넌트에서
const isAuthenticated = useAppSelector(selectIsAuthenticated);
```

### Middleware

```typescript
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import logger from 'redux-logger';

export const store = configureStore({
  reducer: {
    auth: authReducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(logger)
});
```

## 상태 정규화

### Entity Adapter

```typescript
import { createEntityAdapter, createSlice } from '@reduxjs/toolkit';

type User = {
  id: number;
  email: string;
  fullName: string;
};

const usersAdapter = createEntityAdapter<User>();

const usersSlice = createSlice({
  name: 'users',
  initialState: usersAdapter.getInitialState(),
  reducers: {
    userAdded: usersAdapter.addOne,
    usersReceived: usersAdapter.setAll,
    userUpdated: usersAdapter.updateOne,
    userRemoved: usersAdapter.removeOne
  }
});

// Selectors
export const {
  selectAll: selectAllUsers,
  selectById: selectUserById,
  selectIds: selectUserIds
} = usersAdapter.getSelectors((state: RootState) => state.users);
```

## DevTools

### Redux DevTools Extension

```typescript
// 자동으로 활성화됨 (configureStore 사용 시)

// 브라우저에서 확인
// 1. Redux DevTools Extension 설치
// 2. F12 → Redux 탭
```

## 테스팅

### Slice 테스트

```typescript
// src/store/authSlice.test.ts
import { describe, it, expect } from 'vitest';
import authReducer, { setToken, clearError } from './authSlice';

describe('authSlice', () => {
  it('should set token', () => {
    const previousState = { token: null };
    expect(authReducer(previousState, setToken('new-token'))).toEqual({
      token: 'new-token'
    });
  });

  it('should clear error', () => {
    const previousState = { error: 'Some error' };
    expect(authReducer(previousState, clearError())).toEqual({
      error: null
    });
  });
});
```

## 자주 사용하는 패턴

```typescript
// 로딩 상태 관리
const { data, isLoading, error } = useGetUsersQuery();

// Optimistic Updates
const [updateUser] = useUpdateUserMutation();

await updateUser({
  id: userId,
  ...updates
}).unwrap();  // Promise로 변환

// Error Handling
try {
  await dispatch(login({ email, password })).unwrap();
} catch (error) {
  console.error('Login failed:', error);
}
```

## 관련 스킬

- algo-reference-components: React 컴포넌트
- algo-reference-api: API 통신
