<!--
  BERK: this file is YOUR writing exercise. The structure is here, the sentences
  are not. Write each TODO in English, then I will correct it.
  Rule of thumb for a README: WHAT it is -> WHY it exists -> HOW to use it.
-->

# cicd-pipeline-templates

![laravel-example](https://github.com/nrkdrk/cicd-pipeline-templates/actions/workflows/laravel-example.yml/badge.svg)

<!-- TODO (2-3 sentences): what is this repository, and who is it for? -->

## Why

<!-- TODO (3-4 sentences): why copy-paste-ready templates instead of one generic
     pipeline? Mention that every template is proven by a real example app in
     this repository, not by a screenshot. -->

## What is inside

| Stack | GitHub Actions | Azure DevOps | Dockerfile | Example app |
|---|---|---|---|---|
| Laravel (PHP 8.2 / 8.3) | ✅ | ✅ | ✅ multi-stage | `examples/laravel-app` |
| .NET 8 | planned | planned | planned | planned |
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

<!-- TODO: keep the table, write one honest paragraph under it. Which one do you
     reach for at work, and why? Interviewers love this kind of comparison. -->

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
