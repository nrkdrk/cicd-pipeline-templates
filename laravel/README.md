# Laravel pipeline template

This template gives a Laravel project a complete pipeline in three files: it runs
the test suite on two PHP versions and ships a small production image. You copy
the files, change one variable, and the pipeline works.

## Files

| File | Purpose |
|---|---|
| `github-actions.yml` | Test on PHP 8.2 and 8.3, then build and push a signed image |
| `azure-pipelines.yml` | The same pipeline for Azure DevOps |
| `Dockerfile` | Multi-stage build: Composer stage, then a slim FrankenPHP runtime |
| `.dockerignore` | Keeps `vendor`, `.git`, `.env` and developer cache files out of the build context |

## Setup

1. Copy `github-actions.yml` to `.github/workflows/ci.yml`.
2. Copy `Dockerfile` and `.dockerignore` next to your `composer.json`.
3. Set `WORKING_DIRECTORY` if the application is not in the repository root.
4. Commit `composer.lock` - the cache key depends on it.

## Design decisions

- **Multi-stage build.** The first stage installs the dependencies with Composer.
  The final image copies only the result, so Composer, Git and the dev packages
  never reach production. The image stays small and exposes less to an attacker.
  The cost is a slightly longer Dockerfile.

- **No `config:cache` at build time.** The build machine does not know the
  production environment. If the pipeline cached the config during the build, the
  image would carry the wrong values forever. The container caches the config at
  startup instead, when the real environment variables are present.

- **Pull requests never push an image.** A pull request is not a release. The
  tests run on every pull request, but only a push to `main` or a version tag
  produces an image. This keeps the registry clean and stops untrusted code from
  publishing anything.

- **The container runs without a database.** The image has no `.env` file, so
  Laravel would fall back to its own defaults - and the default session driver
  needs a database. The image sets cookie sessions and file cache instead, so the
  container starts alone. Override these at runtime when real infrastructure exists.

## Trade-offs

The runtime is FrankenPHP. The classic alternative is Nginx with PHP-FPM, which
needs two processes and a process manager inside one container. FrankenPHP runs
as a single process, so the Dockerfile stays short. Pick Nginx and PHP-FPM if your
team already knows that setup, or if you need Nginx-specific configuration.
