# Supply chain

A pipeline is a machine that runs other people's code with your credentials.
That is not a criticism of any particular action - it is the shape of the thing.
This repository applies four controls, each answering a different question.

| Control | Question it answers |
|---|---|
| SHA-pinned actions | Is the code in my pipeline the code I reviewed? |
| Vulnerability scan | Does the image I am about to publish contain known holes? |
| SBOM | If a CVE lands tomorrow, can I tell whether I am affected? |
| Provenance attestation | Can someone else prove this image came from this repository? |

## 1. Actions pinned to a commit SHA

`uses: actions/checkout@v4` trusts a tag, and a tag is a pointer the action's
owner can move at any time. Whoever controls that repository - or anyone who
takes it over - can point `v4` at new code, and every pipeline in the world runs
it on the next push, with whatever secrets that job has.

A commit SHA cannot be moved. It is the difference between "the latest version"
and "the version I looked at".

```yaml
# before
uses: actions/checkout@v4

# after
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4
```

Doing this by hand is tedious and easy to get wrong, so this repository ships a
script:

```bash
GITHUB_TOKEN=$(gh auth token) python3 scripts/pin-actions.py
python3 scripts/pin-actions.py --check    # fails if anything is unpinned
```

The trailing comment matters: it keeps the file readable and it lets Dependabot
recognise the pin and open a pull request when the tag moves. Pinning without
automated updates trades one risk for another - frozen dependencies are also
unpatched dependencies. See `.github/dependabot.yml`.

## 2. Scan before pushing, not after

The image is built and loaded locally, scanned with Trivy, and only pushed if the
scan passes. The obvious alternative - push first, scan the published image - is
easier to write and wrong in a specific way: by the time the scan reports, the
vulnerable image already exists in the registry and something may already have
pulled it.

The cost is one extra build step, which is nearly free because the second build
reuses the layer cache from the first.

The scan fails the job on HIGH and CRITICAL findings only. Failing on every
MEDIUM sounds stricter, but a pipeline that is red for reasons nobody intends to
fix is a pipeline people learn to ignore.

## 3. SBOM

A Software Bill of Materials lists what is actually inside the image. Its value
is not on the day it is generated; it is on the day a CVE is published and
somebody asks whether you ship the affected package. Without an SBOM the answer
takes an afternoon of archaeology. With one it is a search.

The SBOM is generated in SPDX format and uploaded as a build artifact, so it is
attached to the run that produced the image rather than living in a wiki that
drifts.

## 4. Build provenance

`actions/attest-build-provenance` records where an image came from - which
repository, which commit, which workflow - and signs that record. Anyone can then
verify it:

```bash
gh attestation verify oci://ghcr.io/OWNER/REPO:TAG --owner OWNER
```

Cosign signing answers a narrower question ("did this key sign this image?").
Provenance answers the more useful one ("what built this, and from what source?").
Both are in the templates.

## What is deliberately missing

- **Secret scanning and dependency review.** GitHub provides both natively; they
  belong in repository settings rather than copied into every workflow file.
- **A private registry policy.** Whether unsigned images may be deployed is a
  cluster admission decision, so it belongs in `k8s-deploy-blueprints`, not here.
- **Signing in the example workflows.** The example pipelines build images but
  never push them, so there is nothing to sign or attest. Those steps exist in
  the templates and are marked as unexercised - this repository does not claim a
  green badge proves them.
