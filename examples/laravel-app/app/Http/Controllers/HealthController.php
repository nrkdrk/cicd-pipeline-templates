<?php

namespace App\Http\Controllers;

use App\Support\Version;
use Illuminate\Http\JsonResponse;

/**
 * Exposes the information a deployment pipeline needs after a rollout:
 * is the app up, and which version is actually running?
 */
final class HealthController
{
    public function __invoke(): JsonResponse
    {
        return response()->json([
            'status' => 'ok',
            // APP_VERSION is injected at build time from the Git tag (see Dockerfile).
            'version' => Version::fromGitTag(env('APP_VERSION')),
        ]);
    }
}
