# Release manifest reference

Every release ships `manifest.json` (schema `edapack.manifest/1`) at the package
root and inside each platform tarball. It is the machine-readable record of what
went into the build.

## Example

```json
{
  "schema": "edapack.manifest/1",
  "package": "verilator-bin",
  "release": {
    "version": "5.038.20260607",
    "tag": "v5.038.20260607",
    "built_at": "2026-06-07T12:00:00Z",
    "trigger": "schedule",
    "recipe_sha": "…"
  },
  "inputs_digest": "sha256:…",
  "inputs": [
    { "name": "verilator", "role": "core", "repo": "https://github.com/verilator/verilator",
      "ref": "master", "resolved_sha": "abc123…", "version": "5.038", "tracked": true },
    { "name": "bitwuzla", "role": "dependency", "repo": "…",
      "ref": "main", "resolved_sha": "def456…", "version": null, "tracked": true }
  ],
  "platforms": [
    { "os": "linux", "arch": "x86_64", "libc": "glibc_2.28",
      "image": "ghcr.io/edapack/manylinux_2_28_x86_64" }
  ],
  "skills": [
    { "name": "verilator", "version": "5.038", "binaries": ["verilator"] }
  ]
}
```

## Fields

| Field | Meaning |
|---|---|
| `package` | The tool package, e.g. `verilator-bin`. |
| `release.version` | `<core_version>.<YYYYMMDD>` — the date component is assigned only when a release is actually published. |
| `release.trigger` | `schedule`, `workflow_dispatch`, or `push`. |
| `release.recipe_sha` | The tool repo's commit at build time (folded into the digest). |
| `inputs_digest` | `sha256:<hex>` over tracked inputs + `recipe_sha`; the change-gate key. |
| `inputs[]` | One entry per input: `name`, `role` (`core`/`dependency`), `repo`, `ref`, `resolved_sha`, `version`, `tracked`. |
| `platform` / `platforms[]` | Per-tarball single `platform`; top-level manifest aggregates all into `platforms[]`. |
| `skills[]` | The Agent Skills shipped in the release (mirrors `skills/index.json`). |

The authoritative schema is
[`schemas/manifest.schema.json`](https://github.com/edapack/edapack-common/blob/v1/schemas/manifest.schema.json).

## Reading a release's inputs

```sh
gh release download v5.038.20260607 --repo edapack/verilator-bin --pattern manifest.json
jq '.inputs[] | {name, version, resolved_sha}' manifest.json
```
