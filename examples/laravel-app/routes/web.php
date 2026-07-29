<?php

use App\Http\Controllers\HealthController;
use Illuminate\Support\Facades\Route;

Route::get('/', fn () => response()->json([
    'app' => config('app.name'),
    'message' => 'CI/CD pipeline templates - example Laravel app',
]));

Route::get('/health', HealthController::class);
