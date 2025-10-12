/**
 * Tests for Input component.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Input from '@/components/common/Input';

describe('Input Component', () => {
  it('renders input with label', () => {
    render(<Input label="Email" />);
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
  });

  it('handles value changes', async () => {
    const handleChange = jest.fn();
    render(<Input label="Email" onChange={handleChange} />);

    const input = screen.getByLabelText('Email');
    await userEvent.type(input, 'test@example.com');

    expect(handleChange).toHaveBeenCalled();
  });

  it('displays error message', () => {
    render(<Input label="Email" error="Invalid email" />);
    expect(screen.getByText('Invalid email')).toBeInTheDocument();
  });

  it('displays helper text when no error', () => {
    render(<Input label="Email" helperText="Enter your email address" />);
    expect(screen.getByText('Enter your email address')).toBeInTheDocument();
  });

  it('applies error styles when error is present', () => {
    render(<Input label="Email" error="Invalid email" />);
    const input = screen.getByLabelText('Email');
    expect(input).toHaveClass('border-red-500');
  });

  it('accepts custom className', () => {
    render(<Input label="Email" className="custom-class" />);
    const input = screen.getByLabelText('Email');
    expect(input).toHaveClass('custom-class');
  });
});
