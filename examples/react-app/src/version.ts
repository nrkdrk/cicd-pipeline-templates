/**
 * Turns a Git tag into a version string the application can report.
 *
 * The pipeline injects the tag as VITE_APP_VERSION at build time, so the running
 * bundle and the image tag always tell the same story. Anything that is not
 * valid SemVer is reported as "dev", because an untagged build is not a release.
 */
const SEM_VER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/

export function versionFromGitTag(tag: string | undefined | null): string {
  const value = (tag ?? '').trim().replace(/^[vV]/, '')

  return SEM_VER.test(value) ? value : 'dev'
}
