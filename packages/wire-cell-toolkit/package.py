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

    version('0.20.0', sha256='7bef9a3709a2f66a1ade5bc942ec7be3449743016ca03d9ff7bd7c8067cbd2cb')
    version('0.19.1', sha256='6b7082ce87e5f433a787ef9a7454f6033d359b0a8d854942181db9fcbb0c5e21')
    version('0.19.0', sha256='8262d313ec8f957b399dfa1bdca268d61110eea946c836fd19440d3764aa43ea')
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
    depends_on('eigen @3.4.0:')
    depends_on('spdlog @1.9.2:')
    depends_on('fftw @3.3.10: ~mpi')
    depends_on('jsoncpp @1.9.4: cxxstd=17')

    # In principle, we can form the list of Boost libs to build based
    # on the list that WCT's waf-tools/wcb.py uses to check for Boost
    # dependencies.  However, beware that developers building against
    # a "full" Boost can add dependency on new Boost libs without
    # noticing that wcb.py does not test for them.  For some details
    # on this issue, see:
    # https://github.com/WireCell/wire-cell-spack/issues/4
    boost_libs = 'date_time exception filesystem graph iostreams math program_options regex system thread'.split()
    boost_variants = '+'.join(boost_libs)
    depends_on('boost @1.78.0: cxxstd=17 +'+boost_variants)

    # we need one or the other
    depends_on('jsonnet @0.18.0: +python', when='+cppjsonnet')
    depends_on('go-jsonnet @0.18.0: +python', when='~cppjsonnet')

    # optional
    depends_on('intel-tbb @2021.3.0: cxxstd=17', when='+tbb')
    # fixme: may need to tell root to use same TBB
    depends_on('root @6.26.00 cxxstd=17', when='+root')
    depends_on('h5cpp ~mpi', when='+hdf')
    depends_on('hdf5 ~mpi', when='+hdf')

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
