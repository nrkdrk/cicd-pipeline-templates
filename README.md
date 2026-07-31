# cicd-pipeline-templates

![laravel-example](https://github.com/nrkdrk/cicd-pipeline-templates/actions/workflows/laravel-example.yml/badge.svg)
![dotnet-example](https://github.com/nrkdrk/cicd-pipeline-templates/actions/workflows/dotnet-example.yml/badge.svg)
![react-example](https://github.com/nrkdrk/cicd-pipeline-templates/actions/workflows/react-example.yml/badge.svg)

Copy-paste CI/CD pipeline templates for Laravel, .NET and React, written for both
GitHub Actions and Azure DevOps. Each template tests the application, builds a
production image and pushes it to a registry. It is for teams that maintain
several projects in different stacks and do not want to write the same pipeline
again every time.

## Why

A pipeline is easy to show and hard to trust. Most examples on the internet look
correct, but nobody can tell whether they still run today. Every template here is
proven by a real application in this repository: the badge above turns green
because `examples/laravel-app` is tested, built into an image, started in a
container and answered a request. Nothing is proven by a screenshot.

The templates are also meant to be copied, not installed. You copy a couple of files,
change one variable, and the pipeline works. There is no shared action, no
private registry and nothing to update later - the copy belongs to your project.

Four real failures were found and fixed while building these templates - a lock
file resolved against the wrong PHP version, a container that needed a database
it did not have, developer cache files leaking into the build context, and a
bundler shipping code that never type-checked. They are documented in
[docs/failure-modes.md](docs/failure-modes.md).

The pipelines pin every action to a commit SHA, scan images before publishing
them, generate an SBOM and attest build provenance. The first scan turned the
build red and produced three findings with three different answers - see
[docs/supply-chain.md](docs/supply-chain.md).

## What is inside

| Stack | GitHub Actions | Azure DevOps | Dockerfile | Example app |
|---|---|---|---|---|
| Laravel (PHP 8.2 / 8.3) | ✅ | ✅ | ✅ multi-stage | `examples/laravel-app` |
| .NET 8 | ✅ | ✅ | ✅ multi-stage | `examples/dotnet-api` |
| React / Vite | ✅ | ✅ | ✅ multi-stage | `examples/react-app` |

## Numbers

Measured on an Apple M-series laptop with Docker Desktop. Your numbers will
differ; the ratios will not.

| Image | Size | Runtime base |
|---|---|---|
| `examples/laravel-app` | 281 MB | FrankenPHP on Alpine |
| `examples/dotnet-api` | 174 MB | ASP.NET 8 on Alpine |
| `examples/react-app` | 76 MB | Nginx (unprivileged) on Alpine |

A naive single-stage Laravel image - the Composer image with the application
copied into it - comes out at 380 MB, so multi-stage saves about a quarter here.
That is a smaller win than the usual marketing suggests, and the reason is worth
knowing: the Composer image is already Alpine-based, so there was never much fat
to remove. The saving is much larger for .NET, where the SDK stage alone is
around 800 MB and none of it reaches the final image. Size is the visible part of
the benefit; the invisible part is that the shipped image contains no package
manager, no compiler and no dev dependencies to exploit.

### Build time, Laravel template

| Scenario | Time |
|---|---|
| Cold build, `--no-cache` | 43.9 s |
| Application source changed | 7.5 s |
| Nothing changed, every layer cached | 3.3 s |

The middle row is the one that matters, because it is what happens on almost
every commit. Copying `composer.json` before the rest of the source means a code
change does not reinstall the dependencies: the 7-second Composer layer is
reused, and only the autoloader and the final copy run again. Note that Docker
compares file contents, not timestamps - `touch` alone will not invalidate a
layer. GitHub Actions gets the same effect across separate runs through
`cache-from: type=gha` in the build job.

## Quick start

```bash
# 1. Copy the workflow into your project
cp laravel/github-actions.yml .github/workflows/ci.yml

# 2. Copy the image definition next to your application
cp laravel/Dockerfile laravel/.dockerignore .

# 3. If your app is not in the repository root, set WORKING_DIRECTORY
#    at the top of the workflow file.
```

## GitHub Actions vs Azure DevOps

Both templates do the same work, and the differences are smaller than they look.
GitHub Actions is shorter to write and its marketplace covers most of the work,
which is why the examples here start with it. Azure DevOps gives more structure:
stages, environments and approvals are part of the product, so larger teams with
release processes often stay on it. The two exist side by side in this repository
because teams rarely get to choose - the platform usually comes with the company.

| | GitHub Actions | Azure DevOps |
|---|---|---|
| Structure | jobs → steps | stages → jobs → steps |
| Caching | `actions/cache` | `Cache@2` task |
| Image tags | `docker/metadata-action` | built by hand from variables |
| Registry auth | `GITHUB_TOKEN` for GHCR | service connection |
| Test reports | job summary | `PublishTestResults@2` |

## Out of scope

Deployment to a cluster lives in [k8s-deploy-blueprints](#) (coming soon).
Secret management is only referenced here, never implemented.

## Copy or call?

These templates are meant to be copied. The other option - one shared workflow
called from many repositories - is also here, as
`.github/workflows/reusable-laravel.yml`, because the choice is real and the
answer changes with the number of repositories you maintain. Copying spreads the
cost of change; sharing concentrates the cost of failure.
[docs/reuse.md](docs/reuse.md) works through both, including the versioning trap
that makes `@main` a bad idea.

## License

MIT