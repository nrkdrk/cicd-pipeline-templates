# cicd-pipeline-templates

![laravel-example](https://github.com/nrkdrk/cicd-pipeline-templates/actions/workflows/laravel-example.yml/badge.svg)
![dotnet-example](https://github.com/nrkdrk/cicd-pipeline-templates/actions/workflows/dotnet-example.yml/badge.svg)

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

The templates are also meant to be copied, not installed. You copy two files,
change one variable, and the pipeline works. There is no shared action, no
private registry and nothing to update later - the copy belongs to your project.

## What is inside

| Stack | GitHub Actions | Azure DevOps | Dockerfile | Example app |
|---|---|---|---|---|
| Laravel (PHP 8.2 / 8.3) | ✅ | ✅ | ✅ multi-stage | `examples/laravel-app` |
| .NET 8 | ✅ | ✅ | ✅ multi-stage | `examples/dotnet-api` |
| React / Vite | planned | planned | planned | planned |

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

## License

MIT