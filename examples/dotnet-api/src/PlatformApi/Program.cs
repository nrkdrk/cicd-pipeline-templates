using PlatformApi;

var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapGet("/", () => Results.Json(new
{
    app = "dotnet-ci-example",
    message = "CI/CD pipeline templates - example .NET API"
}));

// Everything a deployment needs after a rollout: is the API up, and which
// version is actually running? APP_VERSION is injected at build time.
app.MapGet("/health", () => Results.Json(new
{
    status = "ok",
    version = BuildVersion.FromGitTag(Environment.GetEnvironmentVariable("APP_VERSION"))
}));

app.Run();

// Minimal APIs have no Startup class. This makes the generated Program type
// visible to the test project, so WebApplicationFactory can boot the API.
public partial class Program;
