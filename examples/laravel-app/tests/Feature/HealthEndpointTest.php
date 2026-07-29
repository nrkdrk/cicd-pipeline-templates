<?php

namespace Tests\Feature;

use Tests\TestCase;

final class HealthEndpointTest extends TestCase
{
    public function test_the_health_endpoint_reports_the_running_version(): void
    {
        $this->get('/health')
            ->assertOk()
            ->assertJsonStructure(['status', 'version'])
            ->assertJson(['status' => 'ok']);
    }

    public function test_the_home_endpoint_answers_with_json(): void
    {
        $this->get('/')->assertOk()->assertJsonStructure(['app', 'message']);
    }
}
