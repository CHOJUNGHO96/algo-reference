---
name: algo-reference-forms
description: React Hook Form + Zod validation 패턴. Use when creating forms, handling user input, or validating data.
---

# Algo Reference Form Patterns

React Hook Form + Zod를 사용한 폼 처리 및 검증 패턴입니다.

## 기본 폼

### 간단한 로그인 폼

```typescript
// src/components/LoginForm/LoginForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Form, Input, Button } from 'antd';

const loginSchema = z.object({
  email: z.string().email('유효한 이메일을 입력하세요'),
  password: z.string().min(8, '비밀번호는 최소 8자입니다')
});

type LoginFormData = z.infer<typeof loginSchema>;

type LoginFormProps = {
  onSubmit: (data: LoginFormData) => void;
  isLoading?: boolean;
};

export function LoginForm({ onSubmit, isLoading = false }: LoginFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema)
  });

  return (
    <Form onFinish={handleSubmit(onSubmit)} layout="vertical">
      <Form.Item
        label="이메일"
        validateStatus={errors.email ? 'error' : ''}
        help={errors.email?.message}
      >
        <Input type="email" {...register('email')} />
      </Form.Item>

      <Form.Item
        label="비밀번호"
        validateStatus={errors.password ? 'error' : ''}
        help={errors.password?.message}
      >
        <Input.Password {...register('password')} />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={isLoading} block>
          로그인
        </Button>
      </Form.Item>
    </Form>
  );
}
```

## Zod 스키마

### 복잡한 검증

```typescript
const userSchema = z.object({
  email: z.string().email('유효한 이메일을 입력하세요'),
  password: z
    .string()
    .min(8, '비밀번호는 최소 8자입니다')
    .regex(/[A-Z]/, '최소 1개의 대문자가 필요합니다')
    .regex(/[0-9]/, '최소 1개의 숫자가 필요합니다'),
  confirmPassword: z.string(),
  fullName: z.string().min(1, '이름을 입력하세요'),
  age: z.number().min(18, '18세 이상이어야 합니다').optional(),
  agreedToTerms: z.boolean().refine((val) => val === true, {
    message: '약관에 동의해야 합니다'
  })
}).refine((data) => data.password === data.confirmPassword, {
  message: '비밀번호가 일치하지 않습니다',
  path: ['confirmPassword']
});
```

### 중첩 객체

```typescript
const addressSchema = z.object({
  street: z.string(),
  city: z.string(),
  zipCode: z.string().regex(/^\d{5}$/, '5자리 우편번호를 입력하세요')
});

const profileSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  address: addressSchema,
  phoneNumbers: z.array(z.string().regex(/^\d{3}-\d{4}-\d{4}$/))
});
```

## 고급 폼 패턴

### 동적 필드

```typescript
import { useFieldArray } from 'react-hook-form';

const schema = z.object({
  tasks: z.array(
    z.object({
      title: z.string().min(1),
      completed: z.boolean()
    })
  )
});

type FormData = z.infer<typeof schema>;

export function TaskList() {
  const { control, register } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      tasks: [{ title: '', completed: false }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'tasks'
  });

  return (
    <div>
      {fields.map((field, index) => (
        <div key={field.id}>
          <Input {...register(`tasks.${index}.title`)} />
          <input type="checkbox" {...register(`tasks.${index}.completed`)} />
          <Button onClick={() => remove(index)}>삭제</Button>
        </div>
      ))}
      <Button onClick={() => append({ title: '', completed: false })}>
        추가
      </Button>
    </div>
  );
}
```

### Conditional Fields

```typescript
const schema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('personal'),
    ssn: z.string().regex(/^\d{3}-\d{2}-\d{4}$/)
  }),
  z.object({
    type: z.literal('business'),
    ein: z.string().regex(/^\d{2}-\d{7}$/)
  })
]);

export function TaxForm() {
  const { register, watch } = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema)
  });

  const type = watch('type');

  return (
    <div>
      <select {...register('type')}>
        <option value="personal">개인</option>
        <option value="business">사업자</option>
      </select>

      {type === 'personal' && (
        <Input placeholder="SSN" {...register('ssn')} />
      )}

      {type === 'business' && (
        <Input placeholder="EIN" {...register('ein')} />
      )}
    </div>
  );
}
```

## 에러 처리

### 커스텀 에러 메시지

```typescript
const schema = z.object({
  email: z.string().email('이메일 형식이 올바르지 않습니다'),
  age: z.number({
    required_error: '나이를 입력하세요',
    invalid_type_error: '숫자를 입력하세요'
  }).min(18, '18세 이상이어야 합니다')
});
```

### 서버 에러 표시

```typescript
const { setError } = useForm<LoginFormData>({
  resolver: zodResolver(loginSchema)
});

const handleLogin = async (data: LoginFormData) => {
  try {
    await api.login(data);
  } catch (error: any) {
    if (error.response?.status === 401) {
      setError('password', {
        type: 'manual',
        message: '이메일 또는 비밀번호가 올바르지 않습니다'
      });
    }
  }
};
```

## 파일 업로드

```typescript
const schema = z.object({
  avatar: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, '파일을 선택하세요')
    .transform((files) => files[0])
    .refine((file) => file.size <= 5000000, '파일 크기는 5MB 이하여야 합니다')
    .refine(
      (file) => ['image/jpeg', 'image/png'].includes(file.type),
      'JPEG 또는 PNG 파일만 가능합니다'
    )
});

export function AvatarUpload() {
  const { register, handleSubmit } = useForm<{ avatar: File }>({
    resolver: zodResolver(schema)
  });

  const onSubmit = async (data: { avatar: File }) => {
    const formData = new FormData();
    formData.append('avatar', data.avatar);
    await api.uploadAvatar(formData);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="file" accept="image/*" {...register('avatar')} />
      <button type="submit">업로드</button>
    </form>
  );
}
```

## 폼 상태 관리

### Watch 사용

```typescript
const { watch } = useForm();
const password = watch('password');

// 비밀번호 강도 표시
const strength = calculatePasswordStrength(password);
```

### isDirty, isValid

```typescript
const { formState: { isDirty, isValid } } = useForm();

return (
  <Button
    type="primary"
    htmlType="submit"
    disabled={!isDirty || !isValid}
  >
    저장
  </Button>
);
```

## 재사용 가능한 Form Components

### FormField Wrapper

```typescript
type FormFieldProps = {
  label: string;
  name: string;
  type?: 'text' | 'email' | 'password' | 'number';
  error?: string;
  register: UseFormRegister<any>;
};

export function FormField({
  label,
  name,
  type = 'text',
  error,
  register
}: FormFieldProps) {
  return (
    <Form.Item
      label={label}
      validateStatus={error ? 'error' : ''}
      help={error}
    >
      <Input type={type} {...register(name)} />
    </Form.Item>
  );
}

// 사용
<FormField
  label="이메일"
  name="email"
  type="email"
  error={errors.email?.message}
  register={register}
/>
```

## 테스팅

```typescript
// LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('shows validation errors', async () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: /로그인/i }));

    await waitFor(() => {
      expect(screen.getByText('유효한 이메일을 입력하세요')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    const handleSubmit = vi.fn();
    render(<LoginForm onSubmit={handleSubmit} />);

    fireEvent.change(screen.getByLabelText(/이메일/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/비밀번호/i), {
      target: { value: 'password123' }
    });

    fireEvent.click(screen.getByRole('button', { name: /로그인/i }));

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
    });
  });
});
```

## 자주 사용하는 패턴

```typescript
// Reset 폼
const { reset } = useForm();
reset();  // 기본값으로 리셋
reset({ email: '', password: '' });  // 특정 값으로 리셋

// setValue
const { setValue } = useForm();
setValue('email', 'new@example.com');

// Trigger validation
const { trigger } = useForm();
await trigger('email');  // 특정 필드 검증
await trigger();  // 전체 검증
```

## 관련 스킬

- algo-reference-components: React 컴포넌트
- algo-reference-state: Redux 상태 관리
