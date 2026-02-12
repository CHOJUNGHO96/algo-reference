---
name: algo-reference-components
description: React 컴포넌트 및 Ant Design 패턴. Use when creating or modifying React components, UI elements, or layouts.
---

# Algo Reference Component Patterns

React 컴포넌트 및 Ant Design 활용 패턴입니다.

## 컴포넌트 구조

### 기본 컴포넌트

```typescript
// src/components/Button/Button.tsx
import { FC } from 'react';
import { Button as AntButton } from 'antd';
import './Button.css';

type ButtonProps = {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'danger';
};

export const Button: FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false,
  variant = 'primary'
}) => {
  return (
    <AntButton
      type={variant === 'primary' ? 'primary' : 'default'}
      danger={variant === 'danger'}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </AntButton>
  );
};
```

### 폴더 구조

```
src/components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.css
│   └── index.ts
└── UserCard/
    ├── UserCard.tsx
    ├── UserCard.test.tsx
    ├── UserCard.css
    └── index.ts
```

## Ant Design 활용

### Form 컴포넌트

```typescript
// src/components/UserForm/UserForm.tsx
import { FC } from 'react';
import { Form, Input, Button } from 'antd';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email('유효한 이메일을 입력하세요'),
  password: z.string().min(8, '비밀번호는 최소 8자입니다'),
  fullName: z.string().min(1, '이름을 입력하세요')
});

type UserFormData = z.infer<typeof userSchema>;

type UserFormProps = {
  onSubmit: (data: UserFormData) => void;
  isLoading?: boolean;
};

export const UserForm: FC<UserFormProps> = ({ onSubmit, isLoading = false }) => {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema)
  });

  return (
    <Form onFinish={handleSubmit(onSubmit)} layout="vertical">
      <Form.Item
        label="이메일"
        validateStatus={errors.email ? 'error' : ''}
        help={errors.email?.message}
      >
        <Input
          type="email"
          placeholder="user@example.com"
          {...register('email')}
        />
      </Form.Item>

      <Form.Item
        label="비밀번호"
        validateStatus={errors.password ? 'error' : ''}
        help={errors.password?.message}
      >
        <Input.Password
          placeholder="********"
          {...register('password')}
        />
      </Form.Item>

      <Form.Item
        label="이름"
        validateStatus={errors.fullName ? 'error' : ''}
        help={errors.fullName?.message}
      >
        <Input
          placeholder="홍길동"
          {...register('fullName')}
        />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={isLoading} block>
          제출
        </Button>
      </Form.Item>
    </Form>
  );
};
```

### Table 컴포넌트

```typescript
// src/components/UserTable/UserTable.tsx
import { FC } from 'react';
import { Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';

type User = {
  id: number;
  email: string;
  fullName: string;
  isActive: boolean;
  createdAt: string;
};

type UserTableProps = {
  users: User[];
  loading?: boolean;
  onUserClick?: (user: User) => void;
};

export const UserTable: FC<UserTableProps> = ({
  users,
  loading = false,
  onUserClick
}) => {
  const columns: ColumnsType<User> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      sorter: (a, b) => a.id - b.id
    },
    {
      title: '이메일',
      dataIndex: 'email',
      key: 'email',
      sorter: (a, b) => a.email.localeCompare(b.email)
    },
    {
      title: '이름',
      dataIndex: 'fullName',
      key: 'fullName'
    },
    {
      title: '상태',
      dataIndex: 'isActive',
      key: 'isActive',
      render: (isActive: boolean) => (
        <span style={{ color: isActive ? 'green' : 'red' }}>
          {isActive ? '활성' : '비활성'}
        </span>
      )
    },
    {
      title: '생성일',
      dataIndex: 'createdAt',
      key: 'createdAt',
      sorter: (a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
    }
  ];

  return (
    <Table
      columns={columns}
      dataSource={users}
      rowKey="id"
      loading={loading}
      onRow={(record) => ({
        onClick: () => onUserClick?.(record),
        style: { cursor: onUserClick ? 'pointer' : 'default' }
      })}
      pagination={{
        pageSize: 10,
        showSizeChanger: true,
        showTotal: (total) => `총 ${total}개`
      }}
    />
  );
};
```

## Hooks 패턴

### Custom Hook

```typescript
// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { login as loginAction, logout as logoutAction } from '../store/authSlice';

export function useAuth() {
  const dispatch = useDispatch();
  const { user, isAuthenticated, isLoading } = useSelector((state: RootState) => state.auth);

  const login = async (email: string, password: string) => {
    dispatch(loginAction({ email, password }));
  };

  const logout = () => {
    dispatch(logoutAction());
  };

  return { user, isAuthenticated, isLoading, login, logout };
}
```

### useEffect 패턴

```typescript
import { useEffect } from 'react';

export function UserProfile({ userId }: { userId: number }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchUser() {
      try {
        const response = await api.getUser(userId);
        if (!cancelled) {
          setUser(response.data);
        }
      } catch (error) {
        if (!cancelled) {
          console.error('Failed to fetch user:', error);
        }
      }
    }

    fetchUser();

    return () => {
      cancelled = true;  // Cleanup
    };
  }, [userId]);

  if (!user) return <div>Loading...</div>;

  return <div>{user.fullName}</div>;
}
```

## 성능 최적화

### useMemo

```typescript
import { useMemo } from 'react';

export function UserList({ users }: { users: User[] }) {
  const activeUsers = useMemo(
    () => users.filter(user => user.isActive),
    [users]
  );

  return (
    <div>
      {activeUsers.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### useCallback

```typescript
import { useCallback } from 'react';

export function SearchBox({ onSearch }: { onSearch: (query: string) => void }) {
  const handleSearch = useCallback((query: string) => {
    onSearch(query);
  }, [onSearch]);

  return <Input.Search onSearch={handleSearch} />;
}
```

### React.memo

```typescript
import { memo } from 'react';

const UserCard = memo(({ user }: { user: User }) => {
  return (
    <div>
      <h3>{user.fullName}</h3>
      <p>{user.email}</p>
    </div>
  );
});

export default UserCard;
```

## 컴포넌트 패턴

### Compound Components

```typescript
// src/components/Modal/Modal.tsx
type ModalProps = {
  children: React.ReactNode;
  isOpen: boolean;
  onClose: () => void;
};

export const Modal = ({ children, isOpen, onClose }: ModalProps) => {
  if (!isOpen) return null;

  return <div className="modal">{children}</div>;
};

Modal.Header = ({ children }: { children: React.ReactNode }) => (
  <div className="modal-header">{children}</div>
);

Modal.Body = ({ children }: { children: React.ReactNode }) => (
  <div className="modal-body">{children}</div>
);

Modal.Footer = ({ children }: { children: React.ReactNode }) => (
  <div className="modal-footer">{children}</div>
);

// 사용
<Modal isOpen={isOpen} onClose={handleClose}>
  <Modal.Header>제목</Modal.Header>
  <Modal.Body>내용</Modal.Body>
  <Modal.Footer>
    <Button onClick={handleClose}>닫기</Button>
  </Modal.Footer>
</Modal>
```

## 스타일링

### CSS Modules

```typescript
import styles from './Button.module.css';

export const Button = () => {
  return <button className={styles.button}>Click</button>;
};
```

### Ant Design Theme

```typescript
// src/App.tsx
import { ConfigProvider } from 'antd';

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 4
        }
      }}
    >
      {/* 앱 컴포넌트 */}
    </ConfigProvider>
  );
}
```

## 자주 사용하는 명령어

```bash
# 개발 서버
cd frontend && npm run dev

# 테스트
npm run test

# 빌드
npm run build
```

## 관련 스킬

- algo-reference-state: Redux 상태 관리
- algo-reference-forms: 폼 처리 패턴
