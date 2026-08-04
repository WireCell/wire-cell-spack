# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


class Drifires(CMakePackage):
    """drifires calculates drift paths and field responses on electrodes as
    induced current.

    The heavy lifting is done by Garfield++.  libdrifires provides support for
    LAr and parameterized models for geometries related to typical LArTPC
    detectors.  The drifires command line interface produces diagnostic output
    and response data suitable for use with the Wire-Cell Toolkit.
    """

    homepage = "https://github.com/brettviren/drifires"
    git = "https://github.com/brettviren/drifires.git"

    maintainers = ["brettviren"]

    version("master", branch="master")
    version("0.2.0", tag="0.2.0")

    # The CMake build requires C++17.
    depends_on("cxx", type="build")

    depends_on("cmake@3.16:", type="build")

    # Mandatory dependencies.  Each provides a CMake config package which
    # Spack places on CMAKE_PREFIX_PATH, so the WITH_* hints in the CMakeLists
    # are not needed.
    depends_on("nlohmann-json")
    # drifires needs ROOT Core/Graf/Hist/Graf3d/Gpad/Geom/Matrix/MathCore.
    # geom is a variant (default on); the rest are part of a default ROOT.
    depends_on("root +geom")
    depends_on("garfieldpp")

    def cmake_args(self):
        # Belt-and-suspenders: also pass the explicit --with-* install-area
        # hints the CMakeLists exposes.  These are redundant with Spack's
        # CMAKE_PREFIX_PATH but make the dependency resolution robust.
        return [
            self.define("WITH_NLJS", self.spec["nlohmann-json"].prefix),
            self.define("WITH_ROOT", self.spec["root"].prefix),
            self.define("WITH_GARFIELDPP", self.spec["garfieldpp"].prefix),
        ]
