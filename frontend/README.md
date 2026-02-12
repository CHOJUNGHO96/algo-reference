# Algorithm Reference Platform - Frontend

Modern React + TypeScript frontend for the Algorithm Reference Platform.

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 7
- **State Management**: Redux Toolkit with RTK Query
- **Routing**: React Router v6
- **UI Components**: Ant Design
- **Code Highlighting**: Prism.js
- **Form Handling**: React Hook Form + Zod
- **API Client**: Axios (configured in RTK Query)

## Installation

```bash
npm install
```

## Development

```bash
# Start dev server (http://localhost:3000)
npm run dev

# TypeScript build
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Project Structure

See `docs/frontend-architecture.md` for complete documentation.

## Key Features

- 8-point algorithm structure
- GitHub Dark theme
- Syntax-highlighted code blocks with copy button
- RTK Query for API integration
- Responsive design

## TypeScript Interfaces

All interfaces in `src/types/api.ts` match the OpenAPI specification exactly.

## Build Output

```
dist/
├── index.html
├── assets/
│   ├── index-{hash}.css  (~26KB gzipped)
│   └── index-{hash}.js   (~125KB gzipped)
```
