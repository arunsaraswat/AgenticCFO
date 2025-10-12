/**
 * Reusable input component with label and error handling.
 */
import React, { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helperText?: string;
}

/**
 * Input component with Tailwind styling and validation.
 */
const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  className = '',
  id,
  ...props
}) => {
  const inputId = id || `input-${label.toLowerCase().replace(/\s+/g, '-')}`;
  const hasError = Boolean(error);

  return (
    <div className="mb-4">
      <label
        htmlFor={inputId}
        className="block text-sm font-medium text-gray-700 mb-1"
      >
        {label}
      </label>
      <input
        id={inputId}
        className={`
          w-full px-3 py-2 border rounded-lg shadow-sm
          focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
          ${hasError
            ? 'border-red-500 focus:ring-red-500'
            : 'border-gray-300'
          }
          ${className}
        `}
        {...props}
      />
      {hasError && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
      {!hasError && helperText && (
        <p className="mt-1 text-sm text-gray-500">{helperText}</p>
      )}
    </div>
  );
};

export default Input;
