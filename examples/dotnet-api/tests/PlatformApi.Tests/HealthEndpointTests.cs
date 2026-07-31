using System.Net.Http.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace PlatformApi.Tests;

/// <summary>
/// Boots the real application in memory - no container and no open port.
/// </summary>
public class HealthEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public HealthEndpointTests(WebApplicationFactory<Program> factory) => _factory = factory;

    [Fact]
    public async Task The_health_endpoint_reports_the_running_version()
    {
        var response = await _factory.CreateClient().GetAsync("/health");

        response.EnsureSuccessStatusCode();

        var body = await response.Content.ReadFromJsonAsync<HealthResponse>();

        Assert.NotNull(body);
        Assert.Equal("ok", body!.Status);
        Assert.False(string.IsNullOrWhiteSpace(body.Version));
    }

    [Fact]
    public async Task The_home_endpoint_answers_with_json()
    {
        var response = await _factory.CreateClient().GetAsync("/");

        response.EnsureSuccessStatusCode();
        Assert.Equal("application/json", response.Content.Headers.ContentType?.MediaType);
    }

    private sealed record HealthResponse(string Status, string Version);
}
