# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.garfieldpp.package import Garfieldpp as BuiltinGarfieldpp


class Garfieldpp(BuiltinGarfieldpp):
    """Garfield++ with an explicit switch for its optional CUDA/GPU sub-build.

    This wirecell-repo override extends the builtin garfieldpp recipe solely to
    expose a ``cuda`` variant.  Upstream's CMake defaults GARFIELD_WITH_CUDA=ON
    and auto-enables the experimental ``GPU/`` sub-build whenever a CUDA
    compiler (e.g. a system /usr/bin/nvcc) is discovered.  That sub-build is
    fragile -- it compiles .cu sources with nvcc without Garfield's ROOT include
    path, so it fails with "TRandom3.h: No such file or directory" -- and none
    of the wirecell-repo consumers (drifires) need it.  Default it OFF so builds
    are reproducible regardless of whether an nvcc happens to be on PATH.
    """

    variant("cuda", default=False,
            description="Build Garfield++'s optional CUDA/GPU code")

    def cmake_args(self):
        args = super().cmake_args()
        args.append(self.define_from_variant("GARFIELD_WITH_CUDA", "cuda"))
        return args
