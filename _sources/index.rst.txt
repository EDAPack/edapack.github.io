EDAPack
=======

**EDAPack** provides portable, pre-built binary packages of open-source EDA
(Electronic Design Automation) tools.  Each package:

* Runs without requiring a local compiler toolchain or library installation.
* Is published as a self-contained release tarball or zip, downloadable
  directly from GitHub Releases or installable via
  `IVPM <https://github.com/fvutils/ivpm>`_ (``gh-rls`` source).
* Ships with a ``bin/`` directory that IVPM can automatically prepend to
  ``PATH``, so tools are available to downstream tasks immediately.
* Integrates with the `DV Flow <https://dv-flow.github.io/>`_ task framework
  where applicable.

----

Available Packages
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 55 20

   * - Package
     - Description
     - Docs
   * - **iverilog-bin**
     - `Icarus Verilog <https://steveicarus.github.io/iverilog/>`_ Verilog
       simulation compiler and runtime.
     - `iverilog-bin docs <https://edapack.github.io/iverilog-bin/>`_
   * - **verilator-bin**
     - `Verilator <https://www.veripool.org/verilator/>`_ Verilog/SystemVerilog
       simulator/linter, bundled with the Bitwuzla SMT solver and the UVM
       library.
     - `verilator-bin docs <https://edapack.github.io/verilator-bin/>`_
   * - **yosys-bin**
     - `Yosys <https://yosyshq.net/yosys/>`_ open synthesis suite with
       multi-version Python bindings (``pyosys``), the ``yosys-slang``
       SystemVerilog plugin, Boolector SMT solver, and DV Flow integration.
     - `yosys-bin docs <https://edapack.github.io/yosys-bin/>`_
   * - **nextpnr-bin**
     - `nextpnr <https://github.com/YosysHQ/nextpnr>`_ FPGA place-and-route
       tool with iCE40, ECP5, Nexus, and generic backends, plus bundled
       chipdb files.
     - `nextpnr-bin docs <https://edapack.github.io/nextpnr-bin/>`_
   * - **icestorm-bin**
     - `Project IceStorm <https://clifford.at/icestorm/>`_ iCE40 bitstream
       utilities (``icepack``, ``iceprog``, ``icetime``, and friends).
     - `icestorm-bin docs <https://edapack.github.io/icestorm-bin/>`_
   * - **symbiyosys-bin**
     - `SymbiYosys <https://yosyshq.readthedocs.io/projects/symbiyosys/>`_
       formal verification front-end, bundled with Boolector, Yices2, and
       Z3 solvers.
     - `symbiyosys-bin docs <https://edapack.github.io/symbiyosys-bin/>`_
   * - **openroad-bin**
     - `OpenROAD <https://theopenroadproject.org/>`_ autonomous RTL-to-GDS
       physical design flow tool for ASIC implementation.
     - `openroad-bin docs <https://edapack.github.io/openroad-bin/>`_
   * - **opensta-bin**
     - `OpenSTA <https://github.com/The-OpenROAD-Project/OpenSTA>`_ gate-level
       static timing analysis engine.
     - `opensta-bin docs <https://edapack.github.io/opensta-bin/>`_
   * - **ngspice-bin**
     - `ngspice <https://ngspice.sourceforge.io/>`_ mixed-level/mixed-signal
       analog and digital circuit simulator.
     - `ngspice-bin docs <https://edapack.github.io/ngspice-bin/>`_
   * - **gcc-riscv-bin**
     - Complete RISC-V bare-metal cross-compiler toolchain (binutils + GCC +
       newlib) supporting rv32i, rv32imac, rv64i, and rv64imac multilib
       variants.
     - `gcc-riscv-bin docs <https://edapack.github.io/gcc-riscv-bin/>`_
   * - **gdb-multiarch-bin**
     - `GDB <https://www.gnu.org/software/gdb/>`_ built with
       ``--enable-targets=all``, supporting x86/x86_64, RISC-V, ARM/AArch64,
       Xtensa/ESP32, and many more architectures.
     - `gdb-multiarch-bin docs <https://edapack.github.io/gdb-multiarch-bin/>`_
   * - **qemu-riscv**
     - `QEMU <https://www.qemu.org/>`_ RISC-V system emulator for running
       bare-metal and Linux-based RISC-V workloads on an x86_64 host.
     - `qemu-riscv docs <https://edapack.github.io/qemu-riscv/>`_

----

Platform Support
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 18 18 16 18

   * - Package
     - Linux x86_64
     - Linux aarch64
     - macOS arm64
     - Windows x64
   * - **iverilog-bin**
     - ✓
     -
     -
     - ✓
   * - **verilator-bin**
     - ✓
     - ✓
     - ✓
     -
   * - **yosys-bin**
     - ✓
     -
     -
     - ✓
   * - **nextpnr-bin**
     - ✓
     -
     -
     -
   * - **icestorm-bin**
     - ✓
     -
     -
     - ✓
   * - **symbiyosys-bin**
     - ✓
     - ✓
     -
     -
   * - **openroad-bin**
     - ✓
     -
     -
     -
   * - **opensta-bin**
     - ✓
     -
     -
     -
   * - **ngspice-bin**
     - ✓
     -
     -
     -
   * - **gcc-riscv-bin**
     - ✓
     - ✓
     -
     -
   * - **gdb-multiarch-bin**
     - ✓
     - ✓
     -
     -
   * - **qemu-riscv**
     - ✓
     -
     -
     -

----

Quick Start
-----------

**Install from a GitHub Release tarball** — download the appropriate asset
from the package's GitHub Releases page, then extract it::

    tar xf <package>-manylinux_2_28_x86_64-<version>.tar.gz

The extracted directory contains a ``bin/`` subdirectory you can add to
``PATH`` manually, or let IVPM manage it automatically.

Install with IVPM from the published catalog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

EDAPack publishes a top-level package catalog at the site root:

    https://edapack.github.io/ivpm.yaml

The catalog defines one dep-set per tool (``verilator``, ``yosys``,
``nextpnr``, …) plus curated multi-tool *collections* named with a category
prefix:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Collection
     - Tools
   * - ``sim.rtl``
     - Verilator + Icarus Verilog (RTL simulation)
   * - ``sim.analog``
     - ngspice (analog/mixed-signal simulation)
   * - ``flow.fpga.ice40``
     - Yosys + nextpnr + IceStorm (iCE40 bitstream flow)
   * - ``flow.asic``
     - Yosys + OpenROAD + OpenSTA (RTL-to-GDS ASIC flow)
   * - ``verif.formal``
     - Yosys (formal-verification backend)
   * - ``embedded.riscv``
     - gcc-riscv + gdb-multiarch + qemu-riscv (RISC-V bare-metal)

**As a standalone operation** — point ``ivpm update --from`` directly at the
published catalog and select the dep-set to install with ``-d``. No local
``ivpm.yaml`` is required::

    # Install a single tool
    ivpm update --from https://edapack.github.io/ivpm.yaml -d verilator

    # Install a whole collection
    ivpm update --from https://edapack.github.io/ivpm.yaml -d flow.asic

This fetches the named dep-set into ``packages/`` in the current directory.

**By referencing the catalog from your own** ``ivpm.yaml`` — use the
``ivpm.yaml`` source type to pull a named dep-set from the published catalog
into your project. Each ``deps`` entry names the catalog ``url`` and the
``dep-set`` to bundle::

    package:
      name: my-project
      dep-sets:
        - name: default-dev
          deps:
            # Pull a curated collection …
            - name: edapack-asic
              src: ivpm.yaml
              url: https://edapack.github.io/ivpm.yaml
              dep-set: flow.asic
            # … and/or an individual tool
            - name: edapack-verilator
              src: ivpm.yaml
              url: https://edapack.github.io/ivpm.yaml
              dep-set: verilator

    # then run:
    ivpm update

In either case IVPM automatically selects the correct platform asset for each
tool and prepends the package ``bin/`` directory to ``PATH``, so the tools are
available to downstream tasks immediately.

----

Source & Issues
---------------

All package repositories live under the
`EDAPack GitHub organisation <https://github.com/EDAPack>`_.
Bug reports and pull requests are welcome in the individual repositories.

----

Developer Guide
---------------

How the edapack build & release system works, and how to build, release, and
extend the tool packages.

.. toctree::
   :maxdepth: 2

   dev/index
