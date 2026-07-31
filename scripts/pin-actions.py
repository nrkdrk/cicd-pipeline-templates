#!/usr/bin/env python3
"""
Rewrites every "uses: owner/repo@tag" in this repository to a commit SHA.

A tag is a moving pointer: whoever owns the action can move v4 to different code
at any time, and every pipeline that trusts the tag runs that code on the next
push. A commit SHA cannot be moved.

    python3 scripts/pin-actions.py            # rewrite the files
    python3 scripts/pin-actions.py --check    # exit 1 if anything is unpinned

Set GITHUB_TOKEN to avoid the 60 requests per hour limit for anonymous callers:

    GITHUB_TOKEN=$(gh auth token) python3 scripts/pin-actions.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"
USES = re.compile(
    r"(?P<prefix>uses:\s+)(?P<repo>[\w.-]+/[\w.-]+)@(?P<ref>[\w.\-/]+)(?P<comment>\s*#.*)?"
)
SHA = re.compile(r"^[0-9a-f]{40}$")

SEARCH_PATHS = [".github/workflows", "laravel", "dotnet", "react"]
SUFFIXES = {".yml", ".yaml"}


def request(url: str) -> dict | None:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "pin-actions"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 403:
            sys.exit("GitHub API rate limit reached. Set GITHUB_TOKEN and try again.")
        return None


def resolve(repo: str, ref: str) -> str | None:
    """Resolve a tag or branch to the commit SHA it currently points at."""
    reference = request(f"{API}/repos/{repo}/git/ref/tags/{ref}")
    if reference:
        target = reference["object"]
        # Annotated tags point at a tag object, which points at the commit.
        if target["type"] == "tag":
            tag = request(f"{API}/repos/{repo}/git/tags/{target['sha']}")
            return tag["object"]["sha"] if tag else None
        return target["sha"]

    commit = request(f"{API}/repos/{repo}/commits/{ref}")
    return commit["sha"] if commit else None


def process(path: Path, check_only: bool) -> tuple[int, int]:
    original = path.read_text()
    unpinned = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal unpinned
        repo, ref = match["repo"], match["ref"]

        if SHA.match(ref):
            return match.group(0)

        unpinned += 1
        if check_only:
            return match.group(0)

        sha = resolve(repo, ref)
        if sha is None:
            print(f"  could not resolve {repo}@{ref}", file=sys.stderr)
            return match.group(0)

        print(f"  {repo}@{ref} -> {sha[:12]}...")
        return f"{match['prefix']}{repo}@{sha}  # {ref}"

    rewritten = USES.sub(replace, original)

    if not check_only and rewritten != original:
        path.write_text(rewritten)

    return unpinned, len(USES.findall(original))


def main() -> int:
    check_only = "--check" in sys.argv
    root = Path(__file__).resolve().parent.parent

    files = sorted(
        candidate
        for directory in SEARCH_PATHS
        for candidate in (root / directory).glob("*")
        if candidate.suffix in SUFFIXES
    )

    total_unpinned = 0
    for path in files:
        print(f"{path.relative_to(root)}")
        unpinned, _ = process(path, check_only)
        total_unpinned += unpinned

    if check_only and total_unpinned:
        print(f"\n{total_unpinned} action reference(s) are not pinned to a SHA.", file=sys.stderr)
        return 1

    print(f"\n{'Found' if check_only else 'Pinned'} {total_unpinned} reference(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
