using PlatformApi;
using Xunit;

namespace PlatformApi.Tests;

public class BuildVersionTests
{
    [Theory]
    [InlineData("v1.4.0", "1.4.0")]
    [InlineData("2.0.0-rc.1", "2.0.0-rc.1")]
    public void It_normalises_a_git_tag(string tag, string expected)
    {
        Assert.Equal(expected, BuildVersion.FromGitTag(tag));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("not-a-version")]
    public void It_falls_back_to_dev_for_untagged_builds(string? tag)
    {
        Assert.Equal("dev", BuildVersion.FromGitTag(tag));
    }
}
