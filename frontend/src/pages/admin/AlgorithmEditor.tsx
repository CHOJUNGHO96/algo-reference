import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm, useFieldArray, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Input,
  Select,
  Button,
  Form,
  Space,
  Card,
  Tabs,
  message,
  Spin,
  Switch,
} from 'antd';
import {
  PlusOutlined,
  MinusCircleOutlined,
  SaveOutlined,
  EyeOutlined,
} from '@ant-design/icons';
import {
  useCreateAlgorithmMutation,
  useUpdateAlgorithmMutation,
  useGetAlgorithmBySlugQuery,
  useListCategoriesQuery,
} from '../../store/api/algorithmApi';
import type { AlgorithmCreate, AlgorithmUpdate } from '../../types/api';
import './AlgorithmEditor.css';

const { TextArea } = Input;
const { Option } = Select;

// Zod validation schema
const algorithmSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  category_id: z.number({ message: 'Category is required' }),
  difficulty_id: z.number({ message: 'Difficulty is required' }),
  concept_summary: z.string().min(20, 'Concept summary must be at least 20 characters'),
  core_formulas: z.array(
    z.object({
      name: z.string().min(1, 'Formula name is required'),
      formula: z.string().min(1, 'Formula is required'),
      description: z.string().min(1, 'Description is required'),
    })
  ).optional(),
  thought_process: z.string().optional(),
  application_conditions: z.object({
    when_to_use: z.array(z.string()).optional(),
    when_not_to_use: z.array(z.string()).optional(),
  }).optional(),
  time_complexity: z.string().min(1, 'Time complexity is required'),
  space_complexity: z.string().min(1, 'Space complexity is required'),
  problem_types: z.array(
    z.object({
      type: z.string().min(1, 'Problem type is required'),
      leetcode_examples: z.array(z.string()).optional(),
    })
  ).optional(),
  common_mistakes: z.string().optional(),
  is_published: z.boolean().optional(),
});

type AlgorithmFormData = z.infer<typeof algorithmSchema>;

export const AlgorithmEditor = () => {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const isEditMode = !!id;

  const [previewMode, setPreviewMode] = useState(false);
  const [activeTab, setActiveTab] = useState('1');

  // API Hooks
  const { data: categories, isLoading: categoriesLoading } = useListCategoriesQuery();
  const { data: algorithm, isLoading: algorithmLoading } = useGetAlgorithmBySlugQuery(
    id || '',
    { skip: !isEditMode }
  );
  const [createAlgorithm, { isLoading: creating }] = useCreateAlgorithmMutation();
  const [updateAlgorithm, { isLoading: updating }] = useUpdateAlgorithmMutation();

  // Form setup
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
    watch,
  } = useForm<AlgorithmFormData>({
    resolver: zodResolver(algorithmSchema),
    defaultValues: {
      title: '',
      category_id: undefined,
      difficulty_id: undefined,
      concept_summary: '',
      time_complexity: '',
      space_complexity: '',
      core_formulas: [],
      problem_types: [],
      is_published: false,
    },
  });

  // Field arrays for dynamic lists
  const { fields: formulaFields, append: appendFormula, remove: removeFormula } =
    useFieldArray({ control, name: 'core_formulas' });

  const { fields: problemFields, append: appendProblem, remove: removeProblem } =
    useFieldArray({ control, name: 'problem_types' });

  // Load algorithm data in edit mode
  useEffect(() => {
    if (algorithm && isEditMode) {
      reset({
        title: algorithm.title,
        category_id: algorithm.category.id,
        difficulty_id: algorithm.difficulty.id,
        concept_summary: algorithm.concept_summary,
        core_formulas: algorithm.core_formulas || [],
        thought_process: algorithm.thought_process || '',
        application_conditions: algorithm.application_conditions || {
          when_to_use: [],
          when_not_to_use: [],
        },
        time_complexity: algorithm.time_complexity,
        space_complexity: algorithm.space_complexity,
        problem_types: algorithm.problem_types || [],
        common_mistakes: algorithm.common_mistakes || '',
        is_published: algorithm.is_published,
      });
    }
  }, [algorithm, isEditMode, reset]);

  const onSubmit = async (data: AlgorithmFormData) => {
    try {
      if (isEditMode && algorithm) {
        const updateData: AlgorithmUpdate = data;
        await updateAlgorithm({ id: algorithm.id, data: updateData }).unwrap();
        message.success('Algorithm updated successfully!');
      } else {
        const createData: AlgorithmCreate = data as AlgorithmCreate;
        const result = await createAlgorithm(createData).unwrap();
        message.success('Algorithm created successfully!');
        navigate(`/admin/algorithms/${result.id}/edit`);
      }
    } catch (error) {
      const errorMessage = (error as { data?: { detail?: string } })?.data?.detail || 'Failed to save algorithm';
      message.error(errorMessage);
      console.error('Save error:', error);
    }
  };

  if (categoriesLoading || (isEditMode && algorithmLoading)) {
    return (
      <div className="algorithm-editor-loading">
        <Spin size="large" tip="Loading..." />
      </div>
    );
  }

  const formData = watch();

  return (
    <div className="algorithm-editor">
      <div className="editor-header">
        <h1>{isEditMode ? 'Edit Algorithm' : 'Create New Algorithm'}</h1>
        <Space>
          <Button
            icon={<EyeOutlined />}
            onClick={() => setPreviewMode(!previewMode)}
          >
            {previewMode ? 'Edit Mode' : 'Preview Mode'}
          </Button>
          <Button
            type="primary"
            icon={<SaveOutlined />}
            loading={creating || updating}
            onClick={handleSubmit(onSubmit)}
          >
            {isEditMode ? 'Update' : 'Create'}
          </Button>
        </Space>
      </div>

      <div className="editor-content">
        {previewMode ? (
          <div className="preview-panel">
            <Card title={formData.title || 'Untitled Algorithm'}>
              <p><strong>Concept:</strong> {formData.concept_summary}</p>
              <p><strong>Time:</strong> {formData.time_complexity}</p>
              <p><strong>Space:</strong> {formData.space_complexity}</p>
            </Card>
          </div>
        ) : (
          <Form layout="vertical" className="algorithm-form">
            <Tabs activeKey={activeTab} onChange={setActiveTab}>
              {/* Tab 1: Basic Info */}
              <Tabs.TabPane tab="1. Basic Info" key="1">
                <Controller
                  name="title"
                  control={control}
                  render={({ field }) => (
                    <Form.Item
                      label="Title"
                      validateStatus={errors.title ? 'error' : ''}
                      help={errors.title?.message}
                      required
                    >
                      <Input {...field} placeholder="e.g., Two Pointer Technique" />
                    </Form.Item>
                  )}
                />

                <Controller
                  name="category_id"
                  control={control}
                  render={({ field }) => (
                    <Form.Item
                      label="Category"
                      validateStatus={errors.category_id ? 'error' : ''}
                      help={errors.category_id?.message}
                      required
                    >
                      <Select {...field} placeholder="Select category">
                        {categories?.map((cat) => (
                          <Option key={cat.id} value={cat.id}>
                            {cat.name}
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>
                  )}
                />

                <Controller
                  name="difficulty_id"
                  control={control}
                  render={({ field }) => (
                    <Form.Item
                      label="Difficulty"
                      validateStatus={errors.difficulty_id ? 'error' : ''}
                      help={errors.difficulty_id?.message}
                      required
                    >
                      <Select {...field} placeholder="Select difficulty">
                        <Option value={1}>Easy</Option>
                        <Option value={2}>Medium</Option>
                        <Option value={3}>Hard</Option>
                      </Select>
                    </Form.Item>
                  )}
                />

                <Controller
                  name="concept_summary"
                  control={control}
                  render={({ field }) => (
                    <Form.Item
                      label="Concept Summary"
                      validateStatus={errors.concept_summary ? 'error' : ''}
                      help={errors.concept_summary?.message}
                      required
                    >
                      <TextArea
                        {...field}
                        rows={4}
                        placeholder="Brief overview of the algorithm..."
                      />
                    </Form.Item>
                  )}
                />

                <Controller
                  name="is_published"
                  control={control}
                  render={({ field }) => (
                    <Form.Item label="Published">
                      <Switch
                        checked={field.value}
                        onChange={field.onChange}
                        checkedChildren="Yes"
                        unCheckedChildren="No"
                      />
                    </Form.Item>
                  )}
                />
              </Tabs.TabPane>

              {/* Tab 2: Complexity */}
              <Tabs.TabPane tab="2. Complexity" key="2">
                <Controller
                  name="time_complexity"
                  control={control}
                  render={({ field }) => (
                    <Form.Item
                      label="Time Complexity"
                      validateStatus={errors.time_complexity ? 'error' : ''}
                      help={errors.time_complexity?.message}
                      required
                    >
                      <Input {...field} placeholder="e.g., O(n)" />
                    </Form.Item>
                  )}
                />

                <Controller
                  name="space_complexity"
                  control={control}
                  render={({ field }) => (
                    <Form.Item
                      label="Space Complexity"
                      validateStatus={errors.space_complexity ? 'error' : ''}
                      help={errors.space_complexity?.message}
                      required
                    >
                      <Input {...field} placeholder="e.g., O(1)" />
                    </Form.Item>
                  )}
                />
              </Tabs.TabPane>

              {/* Tab 3: Core Formulas */}
              <Tabs.TabPane tab="3. Formulas" key="3">
                <Space direction="vertical" style={{ width: '100%' }}>
                  {formulaFields.map((field, index) => (
                    <Card
                      key={field.id}
                      size="small"
                      title={`Formula ${index + 1}`}
                      extra={
                        <MinusCircleOutlined
                          onClick={() => removeFormula(index)}
                        />
                      }
                    >
                      <Controller
                        name={`core_formulas.${index}.name`}
                        control={control}
                        render={({ field }) => (
                          <Form.Item label="Name">
                            <Input {...field} placeholder="Pattern name" />
                          </Form.Item>
                        )}
                      />
                      <Controller
                        name={`core_formulas.${index}.formula`}
                        control={control}
                        render={({ field }) => (
                          <Form.Item label="Formula">
                            <Input {...field} placeholder="Formula expression" />
                          </Form.Item>
                        )}
                      />
                      <Controller
                        name={`core_formulas.${index}.description`}
                        control={control}
                        render={({ field }) => (
                          <Form.Item label="Description">
                            <TextArea {...field} rows={2} />
                          </Form.Item>
                        )}
                      />
                    </Card>
                  ))}
                  <Button
                    type="dashed"
                    icon={<PlusOutlined />}
                    onClick={() =>
                      appendFormula({ name: '', formula: '', description: '' })
                    }
                  >
                    Add Formula
                  </Button>
                </Space>
              </Tabs.TabPane>

              {/* Tab 4: Thought Process */}
              <Tabs.TabPane tab="4. Thought Process" key="4">
                <Controller
                  name="thought_process"
                  control={control}
                  render={({ field }) => (
                    <Form.Item label="Thought Process (Markdown supported)">
                      <TextArea
                        {...field}
                        rows={10}
                        placeholder="Step-by-step thinking process..."
                      />
                    </Form.Item>
                  )}
                />
              </Tabs.TabPane>

              {/* Tab 5: Problem Types */}
              <Tabs.TabPane tab="5. Problems" key="5">
                <Space direction="vertical" style={{ width: '100%' }}>
                  {problemFields.map((field, index) => (
                    <Card
                      key={field.id}
                      size="small"
                      title={`Problem Type ${index + 1}`}
                      extra={
                        <MinusCircleOutlined
                          onClick={() => removeProblem(index)}
                        />
                      }
                    >
                      <Controller
                        name={`problem_types.${index}.type`}
                        control={control}
                        render={({ field }) => (
                          <Form.Item label="Type">
                            <Input {...field} placeholder="e.g., Pair Sum Problem" />
                          </Form.Item>
                        )}
                      />
                    </Card>
                  ))}
                  <Button
                    type="dashed"
                    icon={<PlusOutlined />}
                    onClick={() =>
                      appendProblem({ type: '', leetcode_examples: [] })
                    }
                  >
                    Add Problem Type
                  </Button>
                </Space>
              </Tabs.TabPane>

              {/* Tab 6: Common Mistakes */}
              <Tabs.TabPane tab="6. Mistakes" key="6">
                <Controller
                  name="common_mistakes"
                  control={control}
                  render={({ field }) => (
                    <Form.Item label="Common Mistakes">
                      <TextArea
                        {...field}
                        rows={8}
                        placeholder="List common pitfalls..."
                      />
                    </Form.Item>
                  )}
                />
              </Tabs.TabPane>
            </Tabs>

            <div className="form-actions">
              <Button onClick={() => navigate('/admin/dashboard')}>
                Cancel
              </Button>
              <Button
                type="primary"
                htmlType="submit"
                loading={creating || updating}
                onClick={handleSubmit(onSubmit)}
              >
                {isEditMode ? 'Update Algorithm' : 'Create Algorithm'}
              </Button>
            </div>
          </Form>
        )}
      </div>
    </div>
  );
};
