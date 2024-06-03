# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class WireCellData(Package):
    """The official 'data' configuration files for Wire-Cell toolkit."""

    homepage = "https://wirecell.bnl.gov"
    url = "https://github.com/WireCell/wire-cell-data/archive/refs/tags/0.1.0.tar.gz"

    license("LGPLv3", checked_by="brettviren")
    maintainers("brettviren")

    version("0.1.0", sha256="cab5d4f4cb39c15bebea361fd0b933e964846207fbac85bb59ea6fdac561fdce")

    def install(self, spec, prefix):
        install("*", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("WIRECELL_PATH", self.prefix);
