# Architecture

The edapack build system separates **what** a tool is made of (declared per
repo) from **how** tools are built and released (shared once in
`edapack-common`).

## The manifest contract

Every release ships `manifest.json` (schema `edapack.manifest/1`). It records
the package, the release metadata, the resolved inputs, the built platforms,
and the shipped skills. The key field is `inputs_digest`:

```
inputs_digest = sha256( recipe_sha + sorted([{name, resolved_sha} for tracked inputs]) )
```

Because the digest folds in both the resolved commit of every *tracked* input
**and** the tool repo's own commit (`recipe_sha`, the "build recipe"), it
changes exactly when a rebuild is warranted: an upstream bump, a dependency
bump, or a change to the build itself. Inputs marked `track: false` are recorded
in the manifest but excluded from the digest, so noisy dependencies don't force
releases.

See {doc}`manifest` for the full field reference.

## The resolve → gate → build → publish flow

The reusable workflow (`edapack-common/.github/workflows/build-release.yml`)
runs four stages:

1. **resolve** — `resolve-inputs.py` reads the repo's `build-inputs.yaml`,
   applies any manual overrides, and resolves each input's policy to a concrete
   commit SHA (via `git ls-remote` / the GitHub releases API — no clone). It
   emits a candidate manifest fragment with the `inputs_digest`.
2. **gate** — `manifest-diff.py` compares the candidate against the previous
   release's `manifest.json` and decides `build_needed`:
   - no prior release, `force`, a `push`, or a pinned `workflow_dispatch` → build
   - a scheduled run whose digest is unchanged → **skip** (no release)
   - a changed digest → build, and the changed inputs go into the release notes
3. **build** (matrix, one job per manylinux image) — runs the tool's
   `scripts/build.sh` inside the rootless builder image. `build.sh` sources
   `build-common.sh` and calls `ec_finalize_release`, which stages skills, ships
   `export.envrc`, and writes the per-platform `manifest.json`.
4. **publish** — merges the per-platform manifests into one top-level
   `manifest.json` and creates the GitHub Release with the tarballs + manifest.

## Why a shared repo

The five tool repos previously shared ~80% of their build scaffolding by
copy-paste (a vendored `stage-skills.py`, near-identical docker wrappers, and
bespoke per-repo version logic). That guarantees drift. `edapack-common`
collapses the shared parts into one versioned source of truth:

- **CI** consumes it as a reusable workflow (`uses: edapack/edapack-common/...@v1`).
- **Local builds** consume it as a sibling checkout (`scripts/local-build.sh`).
- **`build.sh`** consumes it by sourcing `build-common.sh` (the `ec_*` helpers).

Genuinely tool-specific logic (configure flags, dependency build steps) stays in
each repo's `build.sh`; only the shared scaffolding moves out.

## Directory conventions (rootless-safe)

`build-common.sh` enforces three directories so nothing transient lands in the
source tree:

| Var | Meaning | CI | Local |
|---|---|---|---|
| `SRC_DIR` | read-only source checkout | workspace | mounted `:ro` |
| `WORK_DIR` | clones, build trees, staging | `$RUNNER_TEMP/work` | named docker volume |
| `OUT_DIR` | final tarball + manifest | `dist/` | host-owned `dist/` |

This is what makes local manylinux builds leave **zero root-owned files** in the
workspace. See {doc}`local-builds`.
