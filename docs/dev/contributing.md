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
| `docker/Dockerfile` | parametric rootless builder image. |
| `.github/workflows/` | `build-release.yml` (reusable), `builder-images.yml`, `selftest.yml`. |
| `tests/` | pytest (unit/schemas/skills) + shell tests. |

## Versioning & tagging

Tool repos pin `@v1`. Land changes on `main`, then move the floating `v1` tag
forward once `selftest` is green. Cut `@v2` only for breaking changes to the
reusable workflow inputs, the `ec_*` shell API, or the manifest schema.

## Builder images

`docker/Dockerfile` is parametric over `BASE_IMAGE`. `builder-images.yml` builds
and pushes one image per manylinux variant to GHCR weekly and on `docker/**`
changes. When adding a system dependency a tool needs at build time, add it to
the `yum install` line (so builds stay rootless and don't install at runtime).

## Adding a Python tool dependency

Don't. The build path must run inside manylinux containers without pip installs,
so the `scripts/*.py` tools use the standard library only (we hand-parse the
small YAML subset we author). Keep it that way.
