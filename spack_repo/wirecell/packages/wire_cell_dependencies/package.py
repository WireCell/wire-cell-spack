# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class WireCellDependencies(BundlePackage):
    """Only install WireCell Deps."""

    # Add a proper url for your package's homepage here.
    homepage = "https://wirecell.github.io/"

    maintainers = ['brettviren']

    # Only define versions to the extent needed for versioned dependencies.
    version('0.27.1')            # pre fmt v9
    version('0.28.0')            # post fmt v9

    # the rest is copy-paste from wire-cell-toolkit/package.py

    # ----------

    # see eg https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/boost/package.py
    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    # Suggested.  optional but default=True
    variant('tbb', default=True,
            description='Add support for multi-thread execution using TBB')

    # Optional, default=False
    variant('cppjsonnet', default=False,
            description='Use slower C++ Jsonnet instead of Go Jsonnet')
    variant('hdf', default=False,
            description='Add support for HDF5')
    variant('root', default=False,
            description='Add support for ROOT')    
    variant('glpk', default=False,    
            description='Add support for GLPK')

    # just for build time (for waf/wcb)
    depends_on('python', type=('build',)) 
    depends_on('pkgconfig', type=('build',)) 

    # Required

    depends_on('wire-cell-data')

    depends_on('eigen @3.4.0:')

    depends_on('spdlog @1.9.2:')

    # Spack builds spdlog against an "external" fmtlib and does not build
    # against spdlog's bundled fmtlib.  Thie means the version of fmtlib is
    # exposed to the application and spack will tend to use the most recent
    # available.  fmtlib made an API change at v9 that breaks the ability for it
    # to implicitly use ostream insertion operator<<'s.  The new API requires
    # new application code and that code is not compatible with pre-v9 fmtlib.
    # So a mutually-exclusive line in the version sand is required.

    # use of operator<<() is implicit 
    depends_on('fmt @:8.1.1', when='@:0.27.1')  
    # need specialization based on ostream_formatter
    depends_on('fmt @9.0.0:', when='@0.28.0:')  

    depends_on('fftw @3.3.10: ~mpi')
    ## seems jsoncpp builder only supports this variant up to 1.9.2???
    #depends_on('jsoncpp @1.9.4: cxxstd=17')
    depends_on('jsoncpp @1.9.4:')

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

    # We need one or the other.
    depends_on('jsonnet @0.19.1: +python', when='+cppjsonnet')
    depends_on('go-jsonnet @0.19.1: +python', when='~cppjsonnet')


    # Suggested:

    depends_on('intel-tbb @2021.7.0: cxxstd=17', when='+tbb')


    # Optional:

    # ROOT is needed for wire-cell-toolkit/root
    depends_on('root @6.28.04: cxxstd=17', when='+root')
    depends_on('hdf5 ~mpi+threadsafe', when='+hdf')
    depends_on('h5cpp ~mpi', when='+hdf')

    # glpk is needed for wire-cell-toolkit/patrec
    depends_on('glpk', when='+glpk')  

    # TODO: cuda, torch, zmq

    # ----------
