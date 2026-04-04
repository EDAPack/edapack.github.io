EDAPack
=======

**EDAPack** provides portable, pre-built binary packages of open-source EDA
(Electronic Design Automation) tools for Linux.  Each package:

* Runs on any Linux system without a local compiler toolchain or library
  installation.
* Is published as a self-contained release tarball installable with ``pip`` or
  `IVPM <https://github.com/fvutils/ivpm>`_.
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
   * - **yosys-bin**
     - `Yosys <https://yosyshq.net/yosys/>`_ open synthesis suite with
       multi-version Python bindings (``pyosys``), the ``yosys-slang``
       SystemVerilog plugin, Boolector SMT solver, and DV Flow integration.
     - `yosys-bin docs <https://edapack.github.io/yosys-bin/>`_
   * - **verilator-bin**
     - `Verilator <https://www.veripool.org/verilator/>`_ Verilog/SystemVerilog
       simulator/linter, bundled with the Bitwuzla SMT solver and the UVM
       library.
     - `verilator-bin docs <https://edapack.github.io/verilator-bin/>`_
   * - **nextpnr-bin**
     - `nextpnr <https://github.com/YosysHQ/nextpnr>`_ FPGA place-and-route
       tool with iCE40, ECP5, Nexus, and generic backends, plus bundled
       chipdb files.
     - `nextpnr-bin docs <https://edapack.github.io/nextpnr-bin/>`_
   * - **symbiyosys-bin**
     - `SymbiYosys <https://yosyshq.readthedocs.io/projects/symbiyosys/>`_
       formal verification front-end, bundled with Boolector, Yices2, and
       Z3 solvers.
     - `symbiyosys-bin docs <https://edapack.github.io/symbiyosys-bin/>`_
   * - **openroad-bin**
     - `OpenROAD <https://theopenroadproject.org/>`_ autonomous RTL-to-GDS
       physical design flow tool for ASIC implementation.
     - `openroad-bin docs <https://edapack.github.io/openroad-bin/>`_
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

----

Quick Start
-----------

**Install from a GitHub Release tarball**::

    pip install <package>-manylinux-x64-<version>.tar.gz

**Install with IVPM** — add a dependency to your ``ivpm.yaml``::

    package:
      dep-sets:
        - name: default-dev
          deps:
            - name: yosys-bin        # or verilator-bin, nextpnr-bin, …
              src: gh-rls
              url: https://github.com/EDAPack/yosys-bin

    # then run:
    ivpm update

IVPM automatically prepends the package ``bin/`` directory to ``PATH``.

----

Source & Issues
---------------

All package repositories live under the
`EDAPack GitHub organisation <https://github.com/EDAPack>`_.
Bug reports and pull requests are welcome in the individual repositories.
