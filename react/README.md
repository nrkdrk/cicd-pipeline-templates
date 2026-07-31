# React / Vite pipeline template

This template gives a Vite single-page application a complete pipeline in four
files: it lints, type-checks, tests and builds the bundle, then ships it behind
Nginx in an image of about 50 MB. You copy the files, change one variable, and
the pipeline works.

## Files

| File | Purpose |
|---|---|
| `github-actions.yml` | Lint, test, build, then build and push a signed image |
| `azure-pipelines.yml` | The same pipeline for Azure DevOps |
| `Dockerfile` | Multi-stage build: Node stage, then Nginx serving static files |
| `nginx.conf` | SPA fallback, a `/health` endpoint and cache headers |
| `.dockerignore` | Keeps `node_modules` and `dist` out of the build context |

## Setup

1. Copy `github-actions.yml` to `.github/workflows/ci.yml`.
2. Copy `Dockerfile`, `.dockerignore` and `nginx.conf` next to your `package.json`.
3. Set `WORKING_DIRECTORY` if the application is not in the repository root.
4. Commit `package-lock.json` - `npm ci` refuses to run without it.

## Design decisions

- **`npm ci`, never `npm install`.** `npm ci` installs exactly what the lock file
  says and fails if `package.json` and the lock file disagree. `npm install` would
  quietly resolve newer versions on the agent, which means the pipeline could
  build something the developer never tested. The cost is that the lock file has
  to be committed and kept up to date.

- **The version is compiled into the bundle.** A single-page application has no
  server, so it cannot read an environment variable at startup. The pipeline
  passes the Git tag as a build argument and Vite writes it into the bundle. This
  means a new version needs a new build - which is correct for static files, but
  worth knowing before you try to change it at runtime.

- **Nginx runs as a non-root user.** The image is based on the unprivileged Nginx
  image, so the server listens on port 8080 instead of 80. A process that is not
  root cannot bind to a lower port, and it cannot write outside its own files if
  the application is ever compromised.

- **Pull requests never push an image.** A pull request is not a release. The
  tests run on every pull request, but only a push to `main` or a version tag
  produces an image. This keeps the registry clean and stops untrusted code from
  publishing anything.

- **The build type-checks before it bundles.** Vite strips types without checking
  them, so `vite build` alone would happily ship code that does not compile. The
  build script runs `tsc --noEmit` first, which turns a type error into a red
  pipeline instead of a runtime surprise.

## Trade-offs

The image serves static files and nothing else. If you need server-side rendering,
this template is the wrong shape: an SSR application is a Node process, so it
belongs in a Node runtime image with a health endpoint of its own. Split the two
concerns rather than trying to make Nginx render pages.
