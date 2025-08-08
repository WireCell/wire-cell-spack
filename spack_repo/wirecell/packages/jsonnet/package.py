# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack_repo.builtin.build_systems.python import PythonExtension, PythonPipBuilder
from spack.package import *


class Jsonnet(MakefilePackage, PythonExtension):
    """A data templating language for app and tool developers based on JSON"""

    homepage = "https://jsonnet.org/"
    git = "https://github.com/google/jsonnet.git"
    url = "https://github.com/google/jsonnet/archive/refs/tags/v0.18.0.tar.gz"

    maintainers = ["jcpunk"]

    version("master", branch="master")
    version("0.19.1", sha256="f5a20f2dc98fdebd5d42a45365f52fa59a7e6b174e43970fea4f9718a914e887")
    version("0.18.0", sha256="85c240c4740f0c788c4d49f9c9c0942f5a2d1c2ae58b2c71068107bc80a3ced4")
    version("0.17.0", sha256="076b52edf888c01097010ad4299e3b2e7a72b60a41abbc65af364af1ed3c8dbe")
    version('0.16.0', sha256='fa1a4047942797b7c4ed39718a20d63d1b98725fb5cf563efbc1ecca3375426f')

    conflicts("%gcc@:5.4.99", when="@0.18.0:")

    variant("python", default=False, description="Provide Python bindings for jsonnet")
    extends("python", when="+python")
    depends_on("py-setuptools", type=("build",), when="+python")
    depends_on("py-pip", type=("build",), when="+python")
    depends_on("py-wheel", type=("build",), when="+python")

    @property
    def install_targets(self):
        return ["PREFIX={0}".format(self.prefix), "install"]

    @run_after("install")
    def python_install(self):
        if "+python" in self.spec:
            pip_args = PythonPipBuilder.std_args(self)
            args = list(pip_args) + ["--prefix=" + self.prefix, "."]
            pip(*args)
