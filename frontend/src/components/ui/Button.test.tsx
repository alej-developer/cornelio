import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Button from './Button';

describe('Button Component', () => {
  it('renders correctly with given text', () => {
    render(<Button>Secure Action</Button>);
    expect(screen.getByText('Secure Action')).toBeDefined();
  });

  it('renders a spinner and disables button when loading is true', () => {
    const { container } = render(<Button loading>Processing</Button>);
    
    // [ES] Verifica si el elemento spinner está presente / [EN] Verifies if the spinner element is present
    const spinner = container.querySelector('span[class*="spinner"]');
    expect(spinner).not.toBeNull();
    
    // [ES] Verifica si el botón está deshabilitado / [EN] Verifies if the button is disabled
    const button = screen.getByRole('button');
    expect(button.hasAttribute('disabled')).toBe(true);
  });
});
