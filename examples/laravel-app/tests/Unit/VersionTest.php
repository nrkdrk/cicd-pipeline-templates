<?php

namespace Tests\Unit;

use App\Support\Version;
use PHPUnit\Framework\TestCase;

final class VersionTest extends TestCase
{
    public function test_it_strips_the_v_prefix_from_a_git_tag(): void
    {
        $this->assertSame('1.4.0', Version::fromGitTag('v1.4.0'));
    }

    public function test_it_keeps_a_pre_release_suffix(): void
    {
        $this->assertSame('2.0.0-rc.1', Version::fromGitTag('2.0.0-rc.1'));
    }

    public function test_it_falls_back_to_dev_for_untagged_builds(): void
    {
        $this->assertSame('dev', Version::fromGitTag(null));
        $this->assertSame('dev', Version::fromGitTag('not-a-version'));
    }
}
