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

from spack import *


class GoJsonnet(Package):
    """Implementation of Jsonnet in pure Go"""

    homepage = "https://github.com/google/go-jsonnet"
    url      = "https://github.com/google/go-jsonnet/archive/refs/tags/v0.18.0.tar.gz"

    maintainers = ['brettviren']

    version('0.19.1', sha256='7ff57d4d11d8e7a91114acb4506326226ae4ed1954e90d68aeb88b33c35c5b71')
    version('0.18.0', sha256='369af561550ba8cff5dd7dd08a771805a38d795da3285221012cf3a2933b363e')
    version('0.17.0', sha256='4fd04d0c9e38572ef388d28ea6b1ac151b8a9a5026ff94e3a68bdbc18c4db38a')

    depends_on('go', type='build')
    depends_on('git', type='build')
    depends_on('python', when='+python', type=('build', 'run'))

    variant("python", default=False,
            description="Provide Python bindings for go-jsonnet")
    extends("python", when="+python")
    depends_on("py-setuptools", type=("build",), when="+python")
    depends_on("py-pip", type=("build",), when="+python")
    depends_on("py-wheel", type=("build",), when="+python")

    def install(self, spec, prefix):
        # env['GOPATH'] = self.stage.source_path
        env['CGO_CXXFLAGS'] = "-std=c++17 -Wall"
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        git = which('git')
        git('clone','-b','v'+str(spec.version),
            'https://github.com/google/jsonnet.git', 'cpp-jsonnet')
        go = which('go')
        go('build', '-o', prefix.bin, './cmd/jsonnet')
        go('build', '-o', prefix.bin, './cmd/jsonnetfmt')
        go('build', '-o', prefix.bin, './cmd/jsonnet-deps')
        go('build', '-o', 'libgojsonnet.so',
           '-buildmode=c-shared', './c-bindings')

        install("libgojsonnet.so", prefix.lib)
        install("libgojsonnet.h", prefix.include)
        install("cpp-jsonnet/include/libjsonnet.h", prefix.include)


    @run_after("install")
    def python_install(self):
        if "+python" in self.spec:
            args = list(std_pip_args)
            args.append("--prefix=" + self.prefix)
            args.append(".")
            pip(*args)
