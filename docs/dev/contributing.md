# Contributing to edapack-common

`edapack-common` holds the shared build/release logic. Changes here affect every
tool, so it is tested and versioned carefully.

## Running the tests

```sh
make test          # lint (bash -n) + python (pytest) + shell tests
make test-py       # python unit + schema + skills tests
make test-sh       # build-common.sh shell tests
```

The `selftest` workflow runs the same on every push/PR.

## Layout

| Path | What |
|---|---|
| `scripts/*.py` | resolver, manifest, diff, stage-skills (stdlib only — no third-party deps, so they run in the build container). |
| `scripts/*.sh` | `build-common.sh` library, `local-build.sh`, `reset-root-owned.sh`. |
| `schemas/` | JSON Schemas for manifest / build-inputs / skill-manifest. |
| `.github/workflows/` | `build-release.yml` (reusable), `selftest.yml`. |
| `tests/` | pytest (unit/schemas/skills) + shell tests + the build harness. |

## Versioning & tagging

Tool repos pin `@v1`. Land changes on `main`, then move the floating `v1` tag
forward once `selftest` is green. Cut `@v2` only for breaking changes to the
reusable workflow inputs, the `ec_*` shell API, or the manifest schema.

## Build environment

Builds run in the stock `quay.io/pypa/manylinux*` images — there are no custom
images to maintain. Each tool's `build.sh` installs the system packages it needs
at build time under `if [ "${EC_INSTALL_DEPS:-0}" = "1" ]`. When a tool needs a
new system dependency, add it to that block in the tool's `build.sh` (not here).
The shared scripts reach the build via ivpm (`edapack-common` is an ivpm
dependency fetched into `packages/edapack-common`).

## Adding a Python tool dependency

Don't. The build path must run inside manylinux containers without pip installs,
so the `scripts/*.py` tools use the standard library only (we hand-parse the
small YAML subset we author). Keep it that way.
