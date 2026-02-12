/**
 * Unit tests for CodeBlock component
 *
 * Tests syntax highlighting, copy functionality, and rendering variants.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock Prism.js BEFORE importing CodeBlock
vi.mock('prismjs', () => ({
  default: {
    highlight: vi.fn((code) => code), // Return code as-is for testing
    languages: {
      python: {},
      javascript: {},
      cpp: {},
      java: {},
      typescript: {},
      text: {},
    },
  },
}));

// Mock Prism CSS and language components
vi.mock('prismjs/themes/prism-tomorrow.css', () => ({}));
vi.mock('prismjs/components/prism-clike', () => ({}));
vi.mock('prismjs/components/prism-c', () => ({}));
vi.mock('prismjs/components/prism-python', () => ({}));
vi.mock('prismjs/components/prism-cpp', () => ({}));
vi.mock('prismjs/components/prism-java', () => ({}));
vi.mock('prismjs/components/prism-javascript', () => ({}));
vi.mock('prismjs/components/prism-typescript', () => ({}));

import { CodeBlock } from '../code/CodeBlock';

// Mock navigator.clipboard
const mockClipboard = {
  writeText: vi.fn(),
};

Object.assign(navigator, {
  clipboard: mockClipboard,
});

describe('CodeBlock', () => {
  const sampleCode = `def two_pointer(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        return [left, right]`;

  beforeEach(() => {
    mockClipboard.writeText.mockResolvedValue(undefined);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('renders code with syntax highlighting', () => {
    const { container } = render(
      <CodeBlock code={sampleCode} language="python" />
    );

    const codeElement = container.querySelector('code.language-python');
    expect(codeElement).toBeInTheDocument();
  });

  it('displays language label', () => {
    render(<CodeBlock code={sampleCode} language="python" />);
    expect(screen.getByText('python')).toBeInTheDocument();
  });

  it('shows copy button', () => {
    render(<CodeBlock code={sampleCode} language="python" />);
    const copyButton = screen.getByLabelText('Copy code');
    expect(copyButton).toBeInTheDocument();
    expect(screen.getByText('Copy')).toBeInTheDocument();
  });

  it('copies code to clipboard when copy button is clicked', async () => {
    render(<CodeBlock code={sampleCode} language="python" />);

    const copyButton = screen.getByLabelText('Copy code');
    fireEvent.click(copyButton);

    expect(mockClipboard.writeText).toHaveBeenCalledWith(sampleCode);
  });

  it('shows "Copied!" confirmation after copying', async () => {
    render(<CodeBlock code={sampleCode} language="python" />);

    const copyButton = screen.getByLabelText('Copy code');
    fireEvent.click(copyButton);

    await waitFor(() => {
      expect(screen.getByText('Copied!')).toBeInTheDocument();
    });
  });

  it('reverts to "Copy" after 2 seconds', async () => {
    render(<CodeBlock code={sampleCode} language="python" />);

    const copyButton = screen.getByLabelText('Copy code');
    fireEvent.click(copyButton);

    // Verify "Copied!" appears first
    await waitFor(() => {
      expect(screen.getByText('Copied!')).toBeInTheDocument();
    });

    // Wait for 2 seconds timeout to complete
    await new Promise(resolve => setTimeout(resolve, 2100));

    // Should revert back to "Copy"
    expect(screen.getByText('Copy')).toBeInTheDocument();
  }, 10000); // Increase test timeout to 10 seconds

  it('displays explanation when provided', () => {
    const explanation = 'This algorithm uses two pointers to solve the problem efficiently';
    render(
      <CodeBlock
        code={sampleCode}
        language="python"
        explanation={explanation}
      />
    );

    expect(screen.getByText('Explanation:')).toBeInTheDocument();
    expect(screen.getByText(explanation)).toBeInTheDocument();
  });

  it('does not display explanation section when not provided', () => {
    render(<CodeBlock code={sampleCode} language="python" />);
    expect(screen.queryByText('Explanation:')).not.toBeInTheDocument();
  });

  it('shows line numbers by default', () => {
    const { container } = render(
      <CodeBlock code={sampleCode} language="python" />
    );

    const preElement = container.querySelector('pre');
    expect(preElement).toHaveClass('line-numbers');
  });

  it('hides line numbers when showLineNumbers is false', () => {
    const { container } = render(
      <CodeBlock code={sampleCode} language="python" showLineNumbers={false} />
    );

    const preElement = container.querySelector('pre');
    expect(preElement).not.toHaveClass('line-numbers');
  });

  it('handles different programming languages', () => {
    const languages = ['python', 'javascript', 'cpp', 'java', 'typescript'];

    languages.forEach((lang) => {
      const { container } = render(
        <CodeBlock code="console.log('test')" language={lang} />
      );

      expect(container.querySelector(`code.language-${lang}`)).toBeInTheDocument();
      expect(screen.getByText(lang)).toBeInTheDocument();
    });
  });

  it('handles empty code string', () => {
    const { container } = render(
      <CodeBlock code="" language="python" />
    );

    const codeElement = container.querySelector('code');
    expect(codeElement).toBeInTheDocument();
  });

  it('handles code with special characters', () => {
    const specialCode = 'const regex = /[a-z]+/g;\nconst arr = [1, 2, 3];';
    const { container } = render(
      <CodeBlock code={specialCode} language="javascript" />
    );

    const codeElement = container.querySelector('code');
    expect(codeElement).toBeInTheDocument();
  });

  it('handles clipboard write failure gracefully', async () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {});
    mockClipboard.writeText.mockRejectedValue(new Error('Clipboard error'));

    render(<CodeBlock code={sampleCode} language="python" />);

    const copyButton = screen.getByLabelText('Copy code');
    fireEvent.click(copyButton);

    // Wait a bit for async error handling
    await new Promise(resolve => setTimeout(resolve, 100));

    expect(consoleError).toHaveBeenCalledWith(
      'Failed to copy code:',
      expect.any(Error)
    );

    consoleError.mockRestore();
  });

  it('uses fallback language when unsupported language is provided', () => {
    const { container } = render(
      <CodeBlock code="test code" language="unsupported-language" />
    );

    // Should still render with the specified language class
    const codeElement = container.querySelector('code.language-unsupported-language');
    expect(codeElement).toBeInTheDocument();
  });

  it('applies correct CSS classes to container', () => {
    const { container } = render(
      <CodeBlock code={sampleCode} language="python" />
    );

    expect(container.querySelector('.code-block-wrapper')).toBeInTheDocument();
    expect(container.querySelector('.code-block-container')).toBeInTheDocument();
    expect(container.querySelector('.code-block-header')).toBeInTheDocument();
  });

  it('renders multiline code correctly', () => {
    const multilineCode = `line 1
line 2
line 3
line 4`;

    render(<CodeBlock code={multilineCode} language="text" />);

    // All lines should be present in the document
    expect(screen.getByText(/line 1/)).toBeInTheDocument();
  });
});
