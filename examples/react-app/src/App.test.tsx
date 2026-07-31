import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { App } from './App'

describe('App', () => {
  it('renders the running version', () => {
    render(<App />)

    expect(screen.getByTestId('version')).toBeInTheDocument()
  })
})
