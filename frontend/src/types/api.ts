/**
 * TypeScript interfaces matching api-contract.yaml
 * Auto-generated from OpenAPI specification
 */

// Core Models
export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  display_order?: number;
  parent_id?: number | null;
  color?: string;
}

export interface DifficultyLevel {
  id: number;
  name: 'Easy' | 'Medium' | 'Hard';
  color: string;
}

export interface ProgrammingLanguage {
  id: number;
  name: string;
  slug: string;
  extension: string;
  prism_key: string; // Prism.js language key for syntax highlighting
}

export interface CodeTemplate {
  id: number;
  algorithm_id: number;
  language: ProgrammingLanguage;
  code: string;
  explanation?: string;
}

// Algorithm Content Structure (8-point system)
export interface CoreFormula {
  name: string;
  formula: string;
  description: string;
}

export interface ApplicationConditions {
  when_to_use?: string[];
  when_not_to_use?: string[];
}

export interface ProblemType {
  type: string;
  leetcode_examples?: string[];
}

export interface Algorithm {
  id: number;
  title: string;
  slug: string;
  category: Category;
  difficulty: DifficultyLevel;

  // 8-Point Content Structure
  concept_summary: string;
  core_formulas?: CoreFormula[];
  thought_process?: string;
  application_conditions?: ApplicationConditions;
  time_complexity: string;
  space_complexity: string;
  problem_types?: ProblemType[];
  common_mistakes?: string;
  code_templates?: CodeTemplate[];

  is_published: boolean;
  view_count: number;
  created_at: string;
  updated_at: string;
}

// List view (simplified algorithm for cards)
export interface AlgorithmList {
  id: number;
  title: string;
  slug: string;
  category: Category;
  difficulty: DifficultyLevel;
  concept_summary: string;
  time_complexity: string;
  space_complexity: string;
  view_count: number;
}

// Pagination
export interface PaginatedAlgorithms {
  items: AlgorithmList[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Request Models
export interface AlgorithmCreate {
  title: string;
  category_id: number;
  difficulty_id: number;
  concept_summary: string;
  core_formulas?: CoreFormula[];
  thought_process?: string;
  application_conditions?: ApplicationConditions;
  time_complexity: string;
  space_complexity: string;
  problem_types?: ProblemType[];
  common_mistakes?: string;
}

export interface AlgorithmUpdate {
  title?: string;
  category_id?: number;
  difficulty_id?: number;
  concept_summary?: string;
  core_formulas?: CoreFormula[];
  thought_process?: string;
  application_conditions?: ApplicationConditions;
  time_complexity?: string;
  space_complexity?: string;
  problem_types?: ProblemType[];
  common_mistakes?: string;
  is_published?: boolean;
}

export interface CodeTemplateCreate {
  language_id: number;
  code: string;
  explanation?: string;
}

// Auth Models
export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number; // seconds
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface CurrentUser {
  id: number;
  email: string;
  role: string;
}

// Error Models
export interface ErrorResponse {
  detail: string;
  error_code?: string;
}

export interface ValidationErrorItem {
  loc: string[];
  msg: string;
  type: string;
}

export interface ValidationError {
  detail: ValidationErrorItem[];
}

// Query Parameters
export interface ListAlgorithmsParams {
  page?: number;
  size?: number;
  category_id?: number;
  difficulty_id?: number;
  search?: string;
  sort_by?: 'title' | 'view_count' | 'created_at';
  order?: 'asc' | 'desc';
}
