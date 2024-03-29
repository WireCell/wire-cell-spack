# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class WireCellToolkit(Package):
    """Toolkit for Liquid Argon TPC Reconstruction and Visualization ."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://wirecell.github.io/"
    url      = "https://github.com/WireCell/wire-cell-toolkit/archive/refs/tags/0.23.0.tar.gz"

    maintainers = ['brettviren']
    version("0.25.2", sha256="aac849da29092d3397f0130f45c499703496188ad74bd347a3bd154fe23f245d")
    version("0.25.1", sha256="c236758a70fd459824f2f769b1e4e146e8f75965833a5aa8a81f0cf08044f9d6")
    version("0.24.2", sha256="ee8fe70f8ead7b7456bbcd791d8bf1a1cf22c6674df503fb9f93c1d33bfd2a1a")
    version("0.24.1", sha256="0467a4dff51abac3661aa99c5f3cc5de1ba1607a7f357631a2fbf7dcdf01c8a9")
    version("0.24.0", sha256="2a3a62089b40ee1baccdfaf320d3730eed8d301337a616eeb3186097996f3431")
    version("0.23.0", sha256="53712dd4bfea79900fc86eee44779cdd9644be29354569f2b4368a7841a62b57")
    version("0.22.0", sha256="d6c7b4f805fc5d4fbdd4ab0d0b72e3e92a96d458fbc3a03fefed96d0b252931b")
    version('0.21.0', sha256='85c8eed3fcc1637b1d7c1edc0bfb54f0a37c2b9e3bac4f4a3e72b76de4753dd1')
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
    depends_on('boost @1.80.0: cxxstd=17 +'+boost_variants)

    # we need one or the other
    depends_on('jsonnet @0.19.1: +python', when='+cppjsonnet')
    depends_on('go-jsonnet @0.19.1: +python', when='~cppjsonnet')

    # optional
    depends_on('intel-tbb @2021.7.0: cxxstd=17', when='+tbb')
    # fixme: may need to tell root to use same TBB
    depends_on('root @6.28.04 cxxstd=17', when='+root')
    depends_on('hdf5 ~mpi+threadsafe', when='+hdf')
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
