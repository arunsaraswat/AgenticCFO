/**
 * Tests for Button component.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from '@/components/common/Button';

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    await userEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('displays loading state', () => {
    render(<Button isLoading>Click me</Button>);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('disables button when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });

  it('applies primary variant styles by default', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByText('Click me');
    expect(button).toHaveClass('bg-primary-600');
  });

  it('applies secondary variant styles', () => {
    render(<Button variant="secondary">Click me</Button>);
    const button = screen.getByText('Click me');
    expect(button).toHaveClass('bg-gray-200');
  });

  it('applies danger variant styles', () => {
    render(<Button variant="danger">Click me</Button>);
    const button = screen.getByText('Click me');
    expect(button).toHaveClass('bg-red-600');
  });

  it('applies full width styles', () => {
    render(<Button fullWidth>Click me</Button>);
    const button = screen.getByText('Click me');
    expect(button).toHaveClass('w-full');
  });
});
