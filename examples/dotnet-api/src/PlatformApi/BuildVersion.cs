using System.Text.RegularExpressions;

namespace PlatformApi;

/// <summary>
/// Turns a Git tag into a version string the application can report.
///
/// The pipeline tags images from Git tags such as "v1.4.0", so the application
/// and the image always tell the same story. Anything that is not valid SemVer
/// is reported as "dev", because an untagged build is not a release.
/// </summary>
public static class BuildVersion
{
    private const string SemVerPattern = @"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$";

    public static string FromGitTag(string? tag)
    {
        var value = (tag ?? string.Empty).Trim().TrimStart('v', 'V');

        return Regex.IsMatch(value, SemVerPattern) ? value : "dev";
    }
}
