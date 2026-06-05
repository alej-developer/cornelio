import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import MetricCard from './MetricCard';

describe('MetricCard Component', () => {
  it('renders label and value securely', () => {
    render(<MetricCard label="Active Threats" value="0" status="positive" />);
    expect(screen.getByText('Active Threats')).toBeDefined();
    expect(screen.getByText('0')).toBeDefined();
  });

  it('renders subtitle if provided', () => {
    render(
      <MetricCard 
        label="System" 
        value="Online" 
        subtitle="All nodes operational" 
      />
    );
    expect(screen.getByText('All nodes operational')).toBeDefined();
  });
});
