# syntax=docker/dockerfile:1
#
# Multi-stage build for a Vite single-page application.
#
#   docker build -f react/Dockerfile --build-arg APP_VERSION=v1.0.0 -t my-app:1.0.0 examples/react-app
#   docker run --rm -p 8080:8080 my-app:1.0.0
#
# Stage 1 builds the bundle with Node, stage 2 ships static files behind Nginx.
# The final image contains no Node, no node_modules and no source code.

########################  Stage 1: build  ########################
FROM node:25-alpine AS build

WORKDIR /app

# Copy the manifests first so this layer is cached until a dependency changes.
COPY package.json package-lock.json* ./
# "npm ci" installs exactly what the lock file says - never anything newer.
RUN npm ci

COPY . .

# A single-page application has no server, so the version has to be compiled
# into the bundle. Vite only exposes variables that start with VITE_.
ARG APP_VERSION=dev
ENV VITE_APP_VERSION=${APP_VERSION}

RUN npm run build

########################  Stage 2: runtime  ######################
FROM nginxinc/nginx-unprivileged:1.27-alpine AS runtime

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --spider http://localhost:8080/health || exit 1
