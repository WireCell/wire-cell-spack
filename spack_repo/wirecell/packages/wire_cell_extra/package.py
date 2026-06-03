# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class WireCellExtra(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://wirecell.github.io"
    # There is no URL since there is no code to download.

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['brettviren']

    # FIXME: Add proper versions here.
    version('0.0.0')

    # FIXME: Add dependencies if required.
    depends_on('snakemake')

    # There is no need for install() since there is no code.
