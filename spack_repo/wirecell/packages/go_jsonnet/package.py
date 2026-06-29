# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install go-jsonnet
#
# You can edit this file again by typing:
#
#     spack edit go-jsonnet
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
from spack_repo.builtin.build_systems.python import PythonExtension, PythonPipBuilder


class GoJsonnet(Package):
    """Implementation of Jsonnet in pure Go"""

    homepage = "https://github.com/google/go-jsonnet"
    url      = "https://github.com/google/go-jsonnet/archive/refs/tags/v0.18.0.tar.gz"

    maintainers = ['brettviren']

    version("0.22.0", sha256="9c463043a05c1e833c57136521e808ee8df192131f00c636235a2b54823d8c4c")
    version("0.21.0", sha256="ee7aa004e78fb49608bcf28142a7494dc204a07cc07d323dd2cff3d97298c696")
    version("0.20.0", sha256="bf9923a848dba65fa99f6e926221ab4222c2f259ba837d279b43917962bc7d70")
    version('0.19.1', sha256='7ff57d4d11d8e7a91114acb4506326226ae4ed1954e90d68aeb88b33c35c5b71')
    version('0.18.0', sha256='369af561550ba8cff5dd7dd08a771805a38d795da3285221012cf3a2933b363e')
    version('0.17.0', sha256='4fd04d0c9e38572ef388d28ea6b1ac151b8a9a5026ff94e3a68bdbc18c4db38a')

    variant("shared", default=False,
            description="Build the libgojsonnet C-shared library")
    variant("python", default=False,
            description="Provide Python bindings for go-jsonnet")

    # When built +shared, go-jsonnet also installs the reference cpp-jsonnet
    # C++ wrapper (libjsonnet++) linked against the Go engine, plus a
    # libjsonnet.so alias. It is then a drop-in replacement for the C/C++
    # `jsonnet` package's library layout and can satisfy the `libjsonnet`
    # virtual that Jsonnet-consuming packages (e.g. phlex, phlexed) depend on.
    provides("libjsonnet", when="+shared")

    # The command-line programs are pure Go; go and git suffice for them.
    depends_on('go', type='build')
    depends_on('git', type='build')

    # C/C++ compilers are only needed for the cgo-based shared library
    # and for compiling the Python extension.  A CLI-only build (the
    # default) needs neither.
    depends_on('c', type='build', when='+shared')
    depends_on('cxx', type='build', when='+shared')
    depends_on('c', type='build', when='+python')
    depends_on('cxx', type='build', when='+python')

    depends_on('python', when='+python', type=('build', 'run'))
    # The Python bindings in <=0.20.0 use PyEval_CallObject, which was
    # removed in CPython 3.13, so restrict those versions to Python <=3.12.
    depends_on('python@:3.12', when='@:0.20.0 +python', type=('build', 'run'))
    extends("python", when="+python")
    depends_on("py-setuptools", type=("build",), when="+python")
    depends_on("py-pip", type=("build",), when="+python")
    depends_on("py-wheel", type=("build",), when="+python")

    def install(self, spec, prefix):
        # env['GOPATH'] = self.stage.source_path
        mkdirp(prefix.bin)

        # The cpp-jsonnet headers are only consumed by the cgo shared
        # library and by the Python extension build.
        if "+shared" in spec or "+python" in spec:
            git = which('git')
            git('clone', '-b', 'v'+str(spec.version),
                'https://github.com/google/jsonnet.git', 'cpp-jsonnet')

        go = which('go')
        go('build', '-o', prefix.bin, './cmd/jsonnet')
        go('build', '-o', prefix.bin, './cmd/jsonnetfmt')
        go('build', '-o', prefix.bin, './cmd/jsonnet-deps')

        if "+shared" in spec:
            env['CGO_CXXFLAGS'] = "-std=c++17 -Wall"
            mkdirp(prefix.lib)
            mkdirp(prefix.include)
            go('build', '-o', 'libgojsonnet.so',
               '-buildmode=c-shared', './c-bindings')
            install("libgojsonnet.so", prefix.lib)
            install("libgojsonnet.h", prefix.include)
            install("cpp-jsonnet/include/libjsonnet.h", prefix.include)

            # Build the reference C++ wrapper (libjsonnet++) against the Go
            # engine. libjsonnet++.cpp only calls the C ABI that libgojsonnet
            # exports, so it links straight against it. Consumers that use the
            # cpp-jsonnet C++ API (e.g. Phlex's `jsonnet::Jsonnet`) then run on
            # go-jsonnet with no source change -- it is a drop-in libjsonnet++.
            cxx = Executable(env["CXX"])
            cxx("-std=c++17", "-fPIC", "-shared",
                "-Wl,-soname,libjsonnet++.so",
                "-Icpp-jsonnet/include",
                "cpp-jsonnet/cpp/libjsonnet++.cpp",
                "-L" + prefix.lib, "-Wl,-rpath," + prefix.lib, "-lgojsonnet",
                "-o", "libjsonnet++.so")
            install("libjsonnet++.so", prefix.lib)
            install("cpp-jsonnet/include/libjsonnet++.h", prefix.include)

            # Drop-in name compatibility: expose the Go engine under the C
            # library's canonical name, so `find_library(NAMES jsonnet)` and any
            # libjsonnet.so consumer resolve to go-jsonnet.
            with working_dir(prefix.lib):
                if not os.path.exists("libjsonnet.so"):
                    os.symlink("libgojsonnet.so", "libjsonnet.so")


    @run_after("install")
    def python_install(self):
        if "+python" in self.spec:
            pip_args = PythonPipBuilder.std_args(self)
            args = list(pip_args)
            args.append("--prefix=" + self.prefix)
            args.append(".")
            pip(*args)
