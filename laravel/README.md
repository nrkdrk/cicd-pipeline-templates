<!-- BERK: same deal, the TODOs are yours to write in English. -->

# Laravel pipeline template

<!-- TODO (2 sentences): what does this template give a Laravel project? -->

## Files

| File | Purpose |
|---|---|
| `github-actions.yml` | Test on PHP 8.2 and 8.3, then build and push a signed image |
| `azure-pipelines.yml` | The same pipeline for Azure DevOps |
| `Dockerfile` | Multi-stage build: Composer stage, then a slim FrankenPHP runtime |
| `.dockerignore` | Keeps `vendor`, `.git` and `.env` out of the build context |

## Setup

1. Copy `github-actions.yml` to `.github/workflows/ci.yml`.
2. Copy `Dockerfile` and `.dockerignore` next to your `composer.json`.
3. Set `WORKING_DIRECTORY` if the application is not in the repository root.
4. Commit `composer.lock` - the cache key depends on it.

## Design decisions

<!-- TODO: one short paragraph per decision. Say what you chose AND what you
     gave up. These three are already implemented, so just explain them: -->

- **Multi-stage build.** <!-- TODO: why is Composer not in the final image? -->
- **No `config:cache` at build time.** <!-- TODO: what would go wrong? -->
- **Pull requests never push an image.** <!-- TODO: why? -->

## Trade-offs

<!-- TODO: FrankenPHP is used as the runtime. What is the classic alternative,
     and when would you pick it instead? -->
