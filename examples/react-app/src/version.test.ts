import { describe, expect, it } from 'vitest'
import { versionFromGitTag } from './version'

describe('versionFromGitTag', () => {
  it('strips the v prefix from a git tag', () => {
    expect(versionFromGitTag('v1.4.0')).toBe('1.4.0')
  })

  it('keeps a pre-release suffix', () => {
    expect(versionFromGitTag('2.0.0-rc.1')).toBe('2.0.0-rc.1')
  })

  it('falls back to dev for untagged builds', () => {
    expect(versionFromGitTag(undefined)).toBe('dev')
    expect(versionFromGitTag('not-a-version')).toBe('dev')
  })
})
