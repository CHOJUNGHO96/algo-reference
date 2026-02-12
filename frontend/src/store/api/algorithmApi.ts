import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import type {
  Algorithm,
  PaginatedAlgorithms,
  ListAlgorithmsParams,
  AlgorithmCreate,
  AlgorithmUpdate,
  Category,
  ProgrammingLanguage,
  LoginRequest,
  TokenResponse,
  RefreshTokenRequest,
  CurrentUser,
  CodeTemplate,
  CodeTemplateCreate,
} from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const algorithmApi = createApi({
  reducerPath: 'algorithmApi',
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Algorithm', 'Category', 'Language', 'User'],
  endpoints: (builder) => ({
    // Public Algorithm Endpoints
    listAlgorithms: builder.query<PaginatedAlgorithms, ListAlgorithmsParams>({
      query: (params) => ({
        url: '/algorithms',
        params,
      }),
      providesTags: (result) =>
        result
          ? [
              ...result.items.map(({ id }) => ({ type: 'Algorithm' as const, id })),
              { type: 'Algorithm', id: 'LIST' },
            ]
          : [{ type: 'Algorithm', id: 'LIST' }],
    }),

    getAlgorithmBySlug: builder.query<Algorithm, string>({
      query: (slug) => `/algorithms/${slug}`,
      providesTags: (result) =>
        result ? [{ type: 'Algorithm', id: result.id }] : [],
    }),

    // Category Endpoints
    listCategories: builder.query<Category[], void>({
      query: () => '/categories',
      providesTags: [{ type: 'Category', id: 'LIST' }],
    }),

    getCategoryBySlug: builder.query<Category, string>({
      query: (slug) => `/categories/${slug}`,
      providesTags: (result) =>
        result ? [{ type: 'Category', id: result.id }] : [],
    }),

    // Language Endpoints
    listLanguages: builder.query<ProgrammingLanguage[], void>({
      query: () => '/languages',
      providesTags: [{ type: 'Language', id: 'LIST' }],
    }),

    // Auth Endpoints
    login: builder.mutation<TokenResponse, LoginRequest>({
      query: (credentials) => ({
        url: '/auth/login',
        method: 'POST',
        body: credentials,
      }),
    }),

    refreshToken: builder.mutation<TokenResponse, RefreshTokenRequest>({
      query: (body) => ({
        url: '/auth/refresh',
        method: 'POST',
        body,
      }),
    }),

    getCurrentUser: builder.query<CurrentUser, void>({
      query: () => '/auth/me',
      providesTags: [{ type: 'User', id: 'CURRENT' }],
    }),

    // Admin Algorithm Endpoints (JWT required)
    createAlgorithm: builder.mutation<Algorithm, AlgorithmCreate>({
      query: (body) => ({
        url: '/admin/algorithms',
        method: 'POST',
        body,
      }),
      invalidatesTags: [{ type: 'Algorithm', id: 'LIST' }],
    }),

    updateAlgorithm: builder.mutation<
      Algorithm,
      { id: number; data: AlgorithmUpdate }
    >({
      query: ({ id, data }) => ({
        url: `/admin/algorithms/${id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: (_result, _error, { id }) => [
        { type: 'Algorithm', id },
        { type: 'Algorithm', id: 'LIST' },
      ],
    }),

    deleteAlgorithm: builder.mutation<void, number>({
      query: (id) => ({
        url: `/admin/algorithms/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: [{ type: 'Algorithm', id: 'LIST' }],
    }),

    addCodeTemplate: builder.mutation<
      CodeTemplate,
      { algorithmId: number; data: CodeTemplateCreate }
    >({
      query: ({ algorithmId, data }) => ({
        url: `/admin/algorithms/${algorithmId}/templates`,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: (_result, _error, { algorithmId }) => [
        { type: 'Algorithm', id: algorithmId },
      ],
    }),
  }),
});

export const {
  // Public hooks
  useListAlgorithmsQuery,
  useGetAlgorithmBySlugQuery,
  useListCategoriesQuery,
  useGetCategoryBySlugQuery,
  useListLanguagesQuery,

  // Auth hooks
  useLoginMutation,
  useRefreshTokenMutation,
  useGetCurrentUserQuery,

  // Admin hooks
  useCreateAlgorithmMutation,
  useUpdateAlgorithmMutation,
  useDeleteAlgorithmMutation,
  useAddCodeTemplateMutation,
} = algorithmApi;
