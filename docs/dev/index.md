# Developer Guide

How the edapack build & release system works, and how to build, release, and
extend the tool packages (`verilator-bin`, `yosys-bin`, `iverilog-bin`,
`icestorm-bin`, `nextpnr-bin`, …).

## What the build system guarantees

Every binary release produced by the edapack pipeline provides:

1. **A release manifest** (`manifest.json`) recording the exact versions/commits
   of the core source and every tracked dependency that went into the build.
2. **Change-gated weekly releases** — a scheduled build only publishes when an
   input component actually changed since the last release.
3. **Reproducible pinned builds** — any tool can be built at a specific core
   version (e.g. Verilator `v5.038`) on demand.
4. **Rootless local builds** — developers reproduce the manylinux build locally
   without writing root-owned files into the workspace, with a one-command
   cleanup.
5. **A shipped `export.envrc`** — extracted releases drop their `bin/` onto
   `PATH` via direnv.
6. **Shipped Agent Skills** — every release carries the tool's `skills/` so
   agents can drive it.

## How it fits together

```
   tool repo (verilator-bin)            edapack-common (shared)
   ┌────────────────────────┐           ┌──────────────────────────────┐
   │ build-inputs.yaml      │──resolve──▶│ resolve-inputs.py            │
   │ scripts/build.sh ──────┼──sources──▶│ build-common.sh (ec_* libs)  │
   │ scripts/skill-manifest │           │ stage-skills.py              │
   │ scripts/export.envrc   │           │ gen-manifest.py / diff       │
   │ skills/<tool>/         │           │ build-release.yml (reusable) │
   │ .github/workflows/     │──calls───▶│ rootless builder images      │
   │   ci.yml (thin)        │           └──────────────────────────────┘
   └────────────────────────┘
                │
                ▼
        GitHub Release:  <tool>-<platform>-<version>.tar.gz  +  manifest.json
```

The shared logic lives once in
[`edapack-common`](https://github.com/edapack/edapack-common); tool repos stay
thin and declarative. CI consumes it as a reusable workflow; local builds
consume it as a sibling checkout.

## Contents

```{toctree}
:maxdepth: 1

architecture
build-inputs
manifest
local-builds
releasing
skills
adding-a-tool
contributing
```

```{note}
This guide is being written alongside the rollout of the centralized build
system. Pages marked *(planned)* describe behavior that is implemented in
`edapack-common` and being adopted by the tool repos phase by phase.
```
