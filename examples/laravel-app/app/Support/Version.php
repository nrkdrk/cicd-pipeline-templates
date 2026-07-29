<?php

namespace App\Support;

/**
 * Turns a Git tag into a version string the application can report.
 *
 * The pipeline tags images from Git tags such as "v1.4.0", so the app and the
 * image always tell the same story. Anything that is not valid SemVer is
 * reported as "dev", because an untagged build is not a release.
 */
final class Version
{
    private const SEMVER = '/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/';

    public static function fromGitTag(?string $tag): string
    {
        $tag = ltrim(trim((string) $tag), 'vV');

        return preg_match(self::SEMVER, $tag) === 1 ? $tag : 'dev';
    }
}
