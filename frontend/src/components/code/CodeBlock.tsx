import { useState } from 'react';
import { CopyOutlined, CheckOutlined } from '@ant-design/icons';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
// Import base languages first (dependencies)
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-c';
// Then import dependent languages
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-cpp';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-typescript';
import './CodeBlock.css';

interface CodeBlockProps {
  code: string;
  language: string; // e.g., 'python', 'cpp', 'java'
  explanation?: string;
  showLineNumbers?: boolean;
}

export const CodeBlock = ({
  code,
  language,
  explanation,
  showLineNumbers = true
}: CodeBlockProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  // Highlight code using Prism.js
  const highlightedCode = Prism.highlight(
    code,
    Prism.languages[language] || Prism.languages.text,
    language
  );

  return (
    <div className="code-block-wrapper">
      {explanation && (
        <div className="code-explanation">
          <span className="explanation-label">Explanation:</span>
          <span className="explanation-text">{explanation}</span>
        </div>
      )}

      <div className="code-block-container">
        {/* Header with language and copy button */}
        <div className="code-block-header">
          <span className="code-language">{language}</span>
          <button
            className="code-copy-button"
            onClick={handleCopy}
            aria-label="Copy code"
          >
            {copied ? (
              <>
                <CheckOutlined /> Copied!
              </>
            ) : (
              <>
                <CopyOutlined /> Copy
              </>
            )}
          </button>
        </div>

        {/* Code content */}
        <pre className={showLineNumbers ? 'line-numbers' : ''}>
          <code
            className={`language-${language}`}
            dangerouslySetInnerHTML={{ __html: highlightedCode }}
          />
        </pre>
      </div>
    </div>
  );
};
