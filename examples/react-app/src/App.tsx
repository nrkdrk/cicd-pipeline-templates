import { versionFromGitTag } from './version'

export function App() {
  const version = versionFromGitTag(import.meta.env.VITE_APP_VERSION)

  return (
    <main>
      <h1>React CI example</h1>
      <p>
        Running version: <span data-testid="version">{version}</span>
      </p>
    </main>
  )
}
