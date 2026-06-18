# Adding a new tool

Checklist to onboard a new `<tool>-bin` repo onto the edapack build system.

1. **Create the repo** with the standard layout:
   ```
   build-inputs.yaml
   ivpm.yaml                 # lists edapack-common as a dependency
   scripts/build.sh          # sources packages/edapack-common/scripts/build-common.sh
   scripts/skill-manifest.yaml
   scripts/export.envrc      # PATH_add bin
   skills/<tool>/SKILL.md (+ references/, examples/)
   .github/workflows/ci.yml  # thin caller of the reusable workflow
   ```

2. **Declare inputs** in `build-inputs.yaml` (see {doc}`build-inputs`): the core
   source and every tracked dependency, each with a `policy`. And add
   `edapack-common` to `ivpm.yaml` so the shared scripts are fetched into
   `packages/edapack-common`:
   ```yaml
   dep-sets:
   - name: default-dev
     deps:
     - name: edapack-common
       url: https://github.com/edapack/edapack-common.git
   ```

3. **Write `scripts/build.sh`** — do the tool-specific configure/build, then
   call the shared tail:
   ```sh
   source "$EC_COMMON/scripts/build-common.sh"
   ec_init_dirs
   src="$(ec_clone_input <core> <repo> "$EC_CORE_REF")"
   # ... tool-specific build into $release_root ...
   ec_finalize_release "$SRC_DIR" "$release_root" "$CANDIDATE_JSON"
   ec_make_tarball "$release_root" "<tool>-${EC_IMAGE_NAME}-${EC_VERSION}.tar.gz"
   ```

4. **Add the thin `ci.yml`**:
   ```yaml
   on:
     schedule: [{ cron: "0 12 * * 0" }]
     workflow_dispatch:
       inputs:
         core_ref: { type: string }
         input_overrides: { type: string, default: "{}" }
         force: { type: boolean, default: false }
         prerelease: { type: boolean, default: true }
     push:
   jobs:
     build:
       uses: edapack/edapack-common/.github/workflows/build-release.yml@v1
       with:
         package: <tool>-bin
         images: '["manylinux_2_28_x86_64","manylinux_2_34_x86_64"]'
         core_ref: ${{ inputs.core_ref }}
         input_overrides: ${{ inputs.input_overrides || '{}' }}
         force: ${{ inputs.force || false }}
         prerelease: ${{ inputs.prerelease || true }}
   ```

5. **Validate locally**: `scripts/local-build.sh ../<tool>-bin` produces a
   tarball in `dist/` with `manifest.json`, `skills/`, and `export.envrc`, and
   leaves no root-owned files (`find ../<tool>-bin -uid 0` is empty).

6. **Run the acceptance gate** (see the plan's test §3.6): manifest valid,
   change-gate skip/publish, pinned build, skills+envrc present.
