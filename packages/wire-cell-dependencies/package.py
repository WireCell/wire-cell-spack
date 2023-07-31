# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class WireCellDependencies(BundlePackage):
    """Only install WireCell Deps."""

    # Add a proper url for your package's homepage here.
    homepage = "https://wirecell.github.io/"

    maintainers = ['brettviren']

    version('0.0.0')

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

