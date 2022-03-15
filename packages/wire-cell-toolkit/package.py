# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class WireCellToolkit(Package):
    """Toolkit for Liquid Argon TPC Reconstruction and Visualization ."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://wirecell.github.io/"
    url      = "https://github.com/WireCell/wire-cell-toolkit/archive/refs/tags/0.17.1.tar.gz"

    maintainers = ['brettviren']

    version('0.18.0', sha256='9a659d2ac96cff0166c1e78574734981ed1fabe039a2f02376a8b3f04653b6b3')
    version('0.17.1', sha256='4abb1bf16a59815e1702c6c53238c6790ec0872a58f51fd2fc44866419b597e5')

    # optional, default=True
    variant('tbb', default=True,
            description='Support multithread execution')

    # optional, default=False
    variant('cppjsonnet', default=False,
            description='Use slower C++ Jsonnet instead of Go Jsonnet')
    variant('hdf', default=False,
            description='Add support for HDF5')
    variant('root', default=False,
            description='Add support for ROOT')    


    # just for build time (for waf/wcb)
    depends_on('python', type=('build',)) 
    depends_on('pkgconfig', type=('build',)) 

    # required
    depends_on('eigen @3.3.0:')
    depends_on('spdlog @1.9.1:')
    depends_on('fftw @3.3.9: ~mpi')
    depends_on('jsoncpp @1.9.3: cxxstd=17')
    depends_on('boost @1.77.0: cxxstd=17')

    # we need one or the other
    depends_on('jsonnet @0.18.0: +python', when='+cppjsonnet')
    depends_on('go-jsonnet @0.18.0: +python', when='~cppjsonnet')

    # optional
    depends_on('intel-tbb @2021.1.1: cxxstd=17', when='+tbb')
    # fixme: may need to tell root to use same TBB
    depends_on('root cxxstd=17', when='+root')
    depends_on('h5cpp', when='+hdf')

    def install(self, spec, prefix):
        cfg = ["./wcb", "configure", "--prefix={0}".format(prefix)]
        # fixme: honor cppjsonnet variant
        cfg += [
            "--with-jsonnet={0}".format(spec['go-jsonnet'].prefix),
            "--with-jsonnet-lib={0}".format(spec['go-jsonnet'].prefix.lib),
            "--with-jsonnet-libs=gojsonnet",
            "--with-jsonnet-include={0}".format(spec['go-jsonnet'].prefix.include),
            "--boost-mt",
            "--boost-libs={0}".format(spec['boost'].prefix.lib),
            "--boost-includes={0}".format(spec['boost'].prefix.include),
            ]
        bld = ["./wcb", "build", "--notests", "install"]

        bash = which("bash")
        bash("-c", ' '.join(cfg))
        bash("-c", ' '.join(bld))
