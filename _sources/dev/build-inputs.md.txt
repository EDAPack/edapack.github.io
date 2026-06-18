# Authoring `build-inputs.yaml`

Each tool repo declares its input components in a `build-inputs.yaml` at the
repo root (schema `edapack.build-inputs/1`). `resolve-inputs.py` reads it,
resolves every input to a concrete commit, and computes the `inputs_digest`
that gates releases.

## Shape

```yaml
schema: edapack.build-inputs/1
core:
  name: verilator
  repo: https://github.com/verilator/verilator
  policy: branch:master
dependencies:
  - name: bitwuzla
    repo: https://github.com/bitwuzla/bitwuzla
    policy: branch:main
  - name: some-optional-tool
    repo: https://github.com/x/y
    policy: latest-tag
    track: false        # recorded in the manifest, excluded from the digest
```

## Policies

| Policy | Resolves to |
|---|---|
| `branch:<name>` | current HEAD of that branch |
| `tag:<name>` | that exact tag (annotated tags are peeled to the commit) |
| `latest-release` | the repo's latest GitHub *release* tag |
| `latest-tag` | the highest version-sorted tag |

## Overrides

The reusable workflow's `workflow_dispatch` inputs flow into the resolver:

- `core_ref` overrides the `core` input's ref (tag, branch, or raw SHA).
- `input_overrides` is a JSON map `{name: ref}` for dependencies.

An override always wins over the declared `policy`, and a build with any
override set is treated as a *pinned* build (it always builds, regardless of the
change-gate). See {doc}`releasing`.

## `track: false`

Set `track: false` on a dependency whose churn should not, on its own, trigger a
new weekly release. It still appears in `manifest.json` (so the release record is
complete) but is excluded from `inputs_digest`.

## Per-tool inventories

| Tool | core | dependencies |
|---|---|---|
| verilator | verilator (`branch:master`) | bitwuzla |
| yosys | yosys (`latest-release`) | yosys-slang, boolector, sby, mcy, eqy, sv2v |
| iverilog | iverilog (`tag:v13_0`) | — |
| icestorm | icestorm (`branch:master`) | libftdi1 (pinned), libusb (Windows) |
| nextpnr | nextpnr (`latest-tag`) | icestorm-chipdb, prjtrellis, mistral, prjpeppercorn, apicula |
