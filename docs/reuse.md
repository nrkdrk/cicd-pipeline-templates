# Copy a template, or call a shared one?

This repository ships templates you copy. `.github/workflows/reusable-laravel.yml`
is the same pipeline in the other shape: one workflow, called from many
repositories, changed in one place. Both are here because the choice is real, and
because a repository that only argues one side is a brochure rather than a
reference.

## Calling the shared workflow

```yaml
name: ci

on:
  push:
    branches: [main]
    tags: ['v*.*.*']
  pull_request:
    branches: [main]

jobs:
  ci:
    uses: nrkdrk/cicd-pipeline-templates/.github/workflows/reusable-laravel.yml@v1
    with:
      working-directory: .
      image-name: ${{ github.repository }}
      php-versions: '["8.2", "8.3", "8.4"]'
    permissions:
      contents: read
      packages: write
      id-token: write
```

Nine lines instead of a hundred and fifty. That is the entire appeal, and it is
not a small one.

## What each shape actually costs

**Copying spreads the cost of change.** A fix to the Dockerfile has to be applied
to every repository that copied it, by hand, one pull request at a time. With
five projects that is an afternoon. With fifty it never finishes, and the
pipelines drift until nobody can say what any of them do.

**Sharing concentrates the cost of failure.** A shared workflow that breaks
breaks every pipeline that calls it, at the same time, usually while someone is
trying to ship. Worse, a shared workflow that is compromised runs attacker code
in every consuming repository with whatever permissions those jobs hold. Copying
has no such blast radius: a bad copy hurts one project.

**Copying keeps the pipeline readable.** The workflow file sits in the repository
it belongs to. A developer can open it, read it top to bottom, and change one
step without asking anyone. A shared workflow turns that into an input request, a
pull request against another repository, and a version bump - and only if the
maintainer agrees the input is worth having.

**Sharing makes policy possible.** Adding image scanning to fifty copied
pipelines is a project. Adding it to one shared workflow is a commit. If an
organisation needs to guarantee that every image is scanned and every action is
pinned, that guarantee has to live in one place.

## The versioning question

A shared workflow is a dependency, so it needs the discipline of one.

```yaml
uses: owner/repo/.github/workflows/reusable-laravel.yml@v1        # a moving tag
uses: owner/repo/.github/workflows/reusable-laravel.yml@a1b2c3d   # immutable
uses: owner/repo/.github/workflows/reusable-laravel.yml@main      # never do this
```

`@main` means the owner of that repository can change what runs in your pipeline
at any moment - the same problem as an unpinned action, one level up. A moving
major tag such as `@v1` is the usual compromise: consumers get fixes without
acting, and the owner promises not to break the contract inside a major version.
That promise is the actual work. Adding a required input, renaming a job, or
changing a default is a breaking change for every caller, and there is no
compiler to catch it.

## What this repository does

The copy-paste templates are the default, because the intended reader is a person
with a handful of projects on different platforms - some on GitHub Actions, some
on Azure DevOps - who wants a working pipeline today and no dependency on this
repository tomorrow. Half the templates target Azure DevOps, where
`workflow_call` does not exist at all, so a shared-workflow-only repository could
not make its central claim.

The reusable workflow exists for the other case, and for an honest reason: at
roughly ten repositories on one platform, copying stops being cheap. The line is
not exact, but the signal is - the first time you fix the same bug in the fourth
copy, you have already crossed it.

A middle path is worth knowing about: keep the pipeline copied, but move the
expensive, security-relevant parts into a composite action or a shared Dockerfile
base image. Teams end up here more often than at either extreme.

## Limits worth knowing

- A reusable workflow must live in `.github/workflows/`. It cannot sit next to
  the templates it mirrors, which is why this file is not in `laravel/`.
- Calling a workflow from a private repository requires the owner to allow access
  under Settings, Actions, general. Public repositories can be called by anyone.
- Reusable workflows nest at most four levels deep, and a called workflow cannot
  see the caller's `env` block - inputs are the only channel.
- Azure DevOps solves the same problem with template `extends` and repository
  resources, with the same trade-off underneath and none of the same syntax.
