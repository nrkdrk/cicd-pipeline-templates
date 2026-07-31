# .NET pipeline template

This template gives a .NET 8 project a complete pipeline in three files: it runs
the test suite and ships a small production image that starts as a non-root user.
You copy the files, change two variables, and the pipeline works.

## Files

| File | Purpose |
|---|---|
| `github-actions.yml` | Restore, build, test, then build and push a signed image |
| `azure-pipelines.yml` | The same pipeline for Azure DevOps |
| `Dockerfile` | Multi-stage build: SDK stage, then the ASP.NET runtime only |
| `.dockerignore` | Keeps `bin`, `obj` and IDE folders out of the build context |

## Setup

1. Copy `github-actions.yml` to `.github/workflows/ci.yml`.
2. Copy `Dockerfile` and `.dockerignore` next to your solution.
3. Set `WORKING_DIRECTORY` and `TEST_PROJECT` at the top of the workflow file.
4. Adjust the project paths inside the `Dockerfile` to match your solution.

## Design decisions

- **Multi-stage build.** The first stage compiles with the .NET SDK, which is
  around 800 MB. The final image copies only the published output into the ASP.NET
  runtime image, so the compiler, the NuGet cache and the source code never reach
  production. The cost is a slightly longer Dockerfile.

- **The container runs as a non-root user.** The .NET base images already define
  a non-root account, so a single `USER $APP_UID` line is enough. A process that
  is not root cannot write outside its own files if the application is ever
  compromised.

- **Pull requests never push an image.** A pull request is not a release. The
  tests run on every pull request, but only a push to `main` or a version tag
  produces an image. This keeps the registry clean and stops untrusted code from
  publishing anything.

- **No environment settings inside the image.** The build machine does not know
  the production environment. If the pipeline baked `appsettings.Production.json`
  or connection strings into the image, that image would carry the wrong values
  into every environment it is deployed to. The container reads its settings from
  environment variables at startup instead, which is why the same image can run in
  staging and in production without being rebuilt.

## Trade-offs

The image is based on Alpine, which keeps it small but uses musl instead of glibc.
Most applications never notice the difference. Switch to the Debian-based images
(`mcr.microsoft.com/dotnet/aspnet:8.0`) if you depend on a native library that
expects glibc, or if your team already standardised on Debian everywhere.
