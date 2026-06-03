# Local builds

You can reproduce the exact manylinux build locally — in the stock manylinux
image, keeping your source tree clean, with a one-command sudo-free cleanup.

## Prerequisites

- Docker.
- The shared scripts fetched into the tool repo via ivpm:
  ```sh
  cd verilator-bin && ivpm update -a      # populates packages/edapack-common
  ```
  `local-build.sh` itself lives in `edapack-common` (which ivpm fetched into
  `packages/`, or that you checked out as a sibling).

## Build

```sh
edapack-common/scripts/local-build.sh verilator-bin
```

This:

- runs the build in the stock `quay.io/pypa/manylinux_2_28_x86_64` image,
  installing build deps at build time (no custom image);
- mounts your source at `/src` and reads the shared scripts from
  `/src/packages/edapack-common`;
- directs all scratch (clones, build trees, staging) to a named docker volume
  `edapack-<tool>-work` — **never** your workspace;
- lands the tarball + `manifest.json` in the tool's `dist/`, owned by you.

Select a different image with `IMAGE_NAME`:

```sh
IMAGE_NAME=manylinux_2_34_x86_64 scripts/local-build.sh ../verilator-bin
```

Pin an input for a one-off local build:

```sh
core_ref=v5.038 scripts/local-build.sh ../verilator-bin
```

## Cleanup (no sudo)

```sh
scripts/local-build.sh ../verilator-bin clean
```

Removes the `edapack-<tool>-work` volume and `dist/` — the latter via a
throwaway container if it happens to be root-owned, so no `sudo` is needed.

## Migrating a workspace with legacy root-owned files

Older builds (run as root in the container) may have left root-owned directories
in some repos (e.g. `icestorm-bin/{icestorm,libftdi1-*,staging,release}`,
`yosys-bin/cmake-wrapper`). Remove them once, without sudo:

```sh
scripts/reset-root-owned.sh ../icestorm-bin
```

It deletes the known transient build dirs (and sweeps any remaining uid-0
entries) using a throwaway root container over the bind mount, then verifies the
tree is clean.

## Output ownership

The stock manylinux image needs root to install build deps, so the container
runs as root. On a **rootless** daemon (Docker Desktop, rootless Docker, podman)
container-root already maps to your host user, so the outputs in `dist/` are
yours. On a **rootful** daemon the wrapper hands `dist/` back to you with a quick
container `chown` after the build, so either way nothing in your tree needs
`sudo` to read or remove.
