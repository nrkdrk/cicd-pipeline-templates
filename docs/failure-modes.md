# Failure modes

Every failure below actually happened while building this repository. They are
written down because the same four mistakes appear in almost every pipeline, and
because a green badge tells you nothing about what it took to get there.

Each entry follows the same shape: what you see, how to find the cause, why it
happens, and the rule that prevents it next time.

---

## 1. The lock file was resolved with a newer runtime than CI runs

**Symptom.** Tests pass on the developer machine. The CI job fails during
dependency installation with a message about an incompatible set of packages:

```
Your lock file does not contain a compatible set of packages.
Problem 1 - symfony/clock is locked to version v8.1.0 ...
```

**Diagnosis.** Compare the runtime versions on both sides. `php -v` locally,
and the matrix versions in the workflow. If the local version is higher, the
resolver picked packages the CI runner cannot install.

**Root cause.** Composer resolves dependencies against the PHP version it happens
to be running on. A developer on PHP 8.4 produces a lock file that a PHP 8.2
runner cannot satisfy. The lock file describes the developer's laptop, not the
supported runtime.

**Fix.** Pin the platform in `composer.json` so the resolver always targets the
lowest supported version, then regenerate the lock file:

```json
"config": {
    "platform": { "php": "8.2.0" }
}
```

**Rule.** A lock file must reflect the lowest supported runtime, not the machine
that generated it. The same rule has a different name in every ecosystem:
`platform` for Composer, `engines` plus `npm ci` for Node, `global.json` for
.NET. Test the lowest and the highest supported version in CI; the versions in
between rarely surprise you.

---

## 2. The container required a database it did not have

**Symptom.** The image builds. The container starts and stays running. Every
request returns HTTP 500, and the smoke test fails:

```
Database file at path [/app/database/database.sqlite] does not exist
```

**Diagnosis.** Read the application log rather than the container status. A
process that is up is not the same as an application that answers. This is the
whole reason the pipeline curls `/health` instead of checking that the container
is running.

**Root cause.** The image deliberately contains no `.env` file, because
configuration belongs to the environment and secrets never belong in an image.
Without it, Laravel falls back to framework defaults, and the default session
driver in Laravel 11 is `database`. Session middleware then opens a database
connection on every web request, including the health check.

**Fix.** Set defaults in the image that need no external service, and document
that they are meant to be overridden:

```dockerfile
ENV SESSION_DRIVER=cookie \
    CACHE_STORE=file \
    QUEUE_CONNECTION=sync
```

**Rule.** An image must start on its own, with no `.env`, no database and no
network. Anything it cannot do alone belongs behind an environment variable with
a safe default. This is also what makes the same image runnable in staging and
in production without a rebuild.

---

## 3. Developer cache files leaked into the build context

**Symptom.** The build works in CI and fails on the developer machine:

```
Class "NunoMaduro\Collision\Adapters\Laravel\CollisionServiceProvider" not found
Script @php artisan package:discover handling the post-autoload-dump event returned with error code 1
```

**Diagnosis.** Ask what differs between the two build contexts. CI checks out a
clean tree; the laptop has whatever the last local command produced. Here, a
local `composer install` had written `bootstrap/cache/packages.php`, which lists
every package including the dev-only ones.

**Root cause.** `.dockerignore` is not `.gitignore`. Git was ignoring the cache
file, so nobody noticed it existed, but Docker copied it into an image built with
`--no-dev`. The framework then read a package list referring to packages the
image does not contain.

**Fix.** Keep the file out of the context, and delete any leftover during the
build:

```
# .dockerignore
bootstrap/cache/*.php
```

```dockerfile
RUN rm -f bootstrap/cache/*.php \
    && composer dump-autoload --no-dev --optimize --classmap-authoritative \
    && php artisan package:discover --ansi
```

**Rule.** Write `.dockerignore` before the first build, and treat it as a
whitelist problem: everything the image does not need is a liability, not just
for size but for correctness. A build that depends on the state of a laptop is
not reproducible.

---

## 4. The bundler shipped code that did not type-check

**Symptom.** Nothing fails. `vite build` succeeds and produces a bundle, and the
type error only shows up in the browser or, worse, in production.

**Diagnosis.** Run the type checker separately and compare:

```bash
npx tsc --noEmit
```

**Root cause.** Vite strips TypeScript types instead of checking them, because
that is faster and it is the type checker's job. A pipeline that only runs
`vite build` therefore has no type checking at all, even though the project is
written in TypeScript.

**Fix.** Make the build script fail on type errors:

```json
"build": "tsc --noEmit && vite build"
```

**Rule.** Know which guarantee each tool actually gives. A build that succeeds is
not evidence that the code is correct; it is evidence that the bundler was able
to emit files. The pipeline is the place to turn implicit assumptions into
explicit checks.

---

## What these have in common

Three of the four are the same mistake wearing different clothes: **something on
a developer machine was treated as if it were the environment the code runs in.**
A PHP version, a cache file, a set of framework defaults. The fourth is a missing
check rather than a wrong assumption.

That is what a pipeline is for. It is not a build script that happens to run on a
server; it is the first environment that is not yours.
