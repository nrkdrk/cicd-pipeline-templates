# syntax=docker/dockerfile:1
#
# Multi-stage build for a Laravel application.
#
#   docker build -f laravel/Dockerfile --build-arg APP_VERSION=v1.0.0 -t my-app:1.0.0 examples/laravel-app
#   docker run --rm -p 8080:8080 -e APP_KEY="$(php artisan key:generate --show)" my-app:1.0.0
#
# Stage 1 installs the dependencies with Composer, stage 2 ships only the
# runtime. The final image never contains Composer, Git or the dev packages.

########################  Stage 1: build  ########################
FROM composer:2 AS build

WORKDIR /app

# Copy the manifests first so this layer is cached until the dependencies change.
COPY composer.json composer.lock* ./
RUN composer install \
        --no-dev \
        --no-scripts \
        --no-interaction \
        --prefer-dist \
        --optimize-autoloader

# Now copy the application source and finish the installation
# (this runs "artisan package:discover" and writes the package manifest).
COPY . .
RUN composer dump-autoload --no-dev --optimize --classmap-authoritative \
    && php artisan package:discover --ansi

########################  Stage 2: runtime  ######################
FROM dunglas/frankenphp:1-php8.3-alpine AS runtime

# The pipeline passes the Git tag here, so /health can report what is running.
ARG APP_VERSION=dev

ENV APP_VERSION=${APP_VERSION} \
    APP_ENV=production \
    APP_DEBUG=false \
    LOG_CHANNEL=stderr \
    SERVER_NAME=:8080

RUN install-php-extensions opcache pcntl pdo_mysql \
    && apk add --no-cache curl

WORKDIR /app

COPY --from=build --chown=www-data:www-data /app ./

# Laravel needs to write here; nothing else has to be writable.
RUN chmod -R ug+w storage bootstrap/cache

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

# NOTE: "artisan config:cache" is not run here on purpose - it would bake the
# build-time environment into the image. Cache the config at container start
# instead, or run it in an entrypoint once the real env vars are present.
