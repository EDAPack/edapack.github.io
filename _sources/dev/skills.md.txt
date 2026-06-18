# Agent Skills

Every tool ships one or more [Agent Skills](https://github.com/edapack) under
`skills/<name>/`, packaged into every release so agents can drive the tool.
Authoring conventions are documented in the repo-level
`SKILL_DEVELOPMENT_PROCESS.md`; this page covers how skills are validated and
shipped by the build.

## Layout

```
skills/<name>/
  SKILL.md          # frontmatter: name, description, version (+ license)
  references/       # cli-cheatsheet.md, docs-index.md, error-recipes.md
  examples/         # runnable examples, each with run.sh
```

A repo declares which skills to ship in `scripts/skill-manifest.yaml`:

```yaml
skills:
  - name: verilator
    path: skills/verilator
    binaries: [verilator, verilator_coverage, verilator_gantt]
```

## Validation & staging

During the build, `stage-skills.py` (in `edapack-common`):

1. validates each `SKILL.md` frontmatter (`name`, `description`, `version`) and
   that the frontmatter `name` matches the manifest;
2. verifies every declared binary exists in the release `bin/`;
3. copies the skill tree into `<release>/skills/<name>/`;
4. writes `<release>/skills/index.json` (schema `edapack.skills/1`).

## Enforced shipping

The build runs staging in **strict** mode via `ec_finalize_release`, and then
hard-requires `skills/index.json`, `export.envrc`, and `manifest.json` to be
present before packaging. A missing skill, a missing binary, or a missing
`export.envrc` **fails the build** — shipping skills and the envrc is an
invariant, not an optional step.
