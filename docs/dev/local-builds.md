# Local builds (rootless)

You can reproduce the exact manylinux build locally — without writing
root-owned files into your workspace, and with a one-command cleanup.

## Prerequisites

- Docker.
- A checkout of [`edapack-common`](https://github.com/edapack/edapack-common),
  ideally as a sibling of the tool repos.

## Build

```sh
# from the edapack-common checkout:
scripts/local-build.sh ../verilator-bin
```

This:

- runs the build inside the rootless manylinux builder image
  (`ghcr.io/edapack/manylinux_2_28_x86_64` by default);
- mounts your source **read-only** at `/src`;
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

Removes the `edapack-<tool>-work` volume and `dist/`. Because nothing root-owned
was ever written, no `sudo` is needed.

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

## How rootlessness is achieved

On a **rootful** daemon (most CI, including GitHub Actions), the container runs
as your host UID (`--user`) so its writes are host-owned. On a **rootless**
daemon, container-root already maps to your host user, so the wrapper detects
this and omits `--user` (forcing it would break bind-mount writes). Override the
detection with `EC_RUN_AS_USER=1` or `0` if needed.
