# Releasing

Releases are produced by the reusable `build-release` workflow in
`edapack-common`. A tool's `ci.yml` is a thin caller.

## Weekly change-gated releases

Each tool runs on a weekly schedule. On a scheduled run the pipeline:

1. resolves every input in `build-inputs.yaml` to a concrete commit;
2. computes the `inputs_digest`;
3. compares it to the previous release's `manifest.json`.

If the digest is unchanged, **no release is published** — a Sunday with no
upstream movement produces nothing, by design. If any tracked input (or the
build recipe) changed, it builds and publishes, and the release notes list
exactly which inputs moved.

The version is `<core_version>.<YYYYMMDD>`, with the date assigned only when a
release is actually cut.

## Manual pinned builds

To build a specific version on demand, run the tool's workflow from the Actions
UI (`workflow_dispatch`) with:

| Input | Effect |
|---|---|
| `core_ref` | Build this core ref (tag/branch/SHA), e.g. `v5.038`. |
| `input_overrides` | JSON map `{name: ref}` to pin dependencies. |
| `force` | Build even if the change-gate says nothing changed. |
| `prerelease` | Mark the release prerelease (default `true`). |

A dispatch with any `core_ref`/`input_overrides` set is a *pinned* build and
always proceeds regardless of the gate. The resulting `manifest.json` records
the pinned refs, so the build is fully reproducible.

## Build targets (x86_64 / aarch64 / macOS)

A tool's `ci.yml` chooses what to build via one of two `with:` inputs to the
reusable workflow:

- **`images`** — the simple case: a JSON array of x86_64 manylinux short-names.
  Each becomes a `docker run quay.io/pypa/<name>` job on `ubuntu-latest`.
- **`targets`** — the rich case (overrides `images`): a JSON array of objects
  `{name, runs-on, kind: docker|native, image?}`. Use it for **aarch64**
  (`kind: docker` on an arm Linux runner, e.g. `ubuntu-24.04-arm`) and **macOS**
  (`kind: native`, e.g. `runs-on: macos-14`, which runs `build.sh` directly and
  provisions deps via Homebrew). `verilator-bin/.github/workflows/ci.yml` is the
  worked example (x86_64 + aarch64 manylinux + native macOS-arm64).

aarch64 Linux runners are free on public repos; native macOS targets only work
for tools whose `build.sh` has a macOS path.

## What a release contains

```
<tool>-<platform>-<version>.tar.gz      # one per manylinux image
<tool>-<platform>-<version>.tar.gz.sha256
manifest.json                            # top-level, aggregates all platforms
```

Each tarball additionally contains its own `manifest.json`, `export.envrc`, and
`skills/` tree.
