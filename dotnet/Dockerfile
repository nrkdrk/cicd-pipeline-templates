# syntax=docker/dockerfile:1
#
# Multi-stage build for a .NET 8 API.
#
#   docker build -f dotnet/Dockerfile --build-arg APP_VERSION=v1.0.0 -t my-api:1.0.0 examples/dotnet-api
#   docker run --rm -p 8080:8080 my-api:1.0.0
#
# Stage 1 compiles with the SDK, stage 2 ships only the ASP.NET runtime.
# The final image contains no compiler, no NuGet cache and no source code.

########################  Stage 1: build  ########################
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build

WORKDIR /src

# Copy the project file first so the restore layer is cached until a
# dependency changes - the same trick as composer.json in the Laravel template.
COPY src/PlatformApi/PlatformApi.csproj src/PlatformApi/
RUN dotnet restore src/PlatformApi/PlatformApi.csproj

# Now copy the source and publish.
COPY . .
RUN dotnet publish src/PlatformApi/PlatformApi.csproj \
        --configuration Release \
        --no-restore \
        --output /app/publish

########################  Stage 2: runtime  ######################
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime

# The pipeline passes the Git tag here, so /health can report what is running.
ARG APP_VERSION=dev

ENV APP_VERSION=${APP_VERSION} \
    ASPNETCORE_ENVIRONMENT=Production \
    ASPNETCORE_URLS=http://+:8080 \
    DOTNET_RUNNING_IN_CONTAINER=true

RUN apk add --no-cache curl

WORKDIR /app

COPY --from=build /app/publish ./

# The .NET images define a non-root user for exactly this purpose.
USER $APP_UID

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "PlatformApi.dll"]
