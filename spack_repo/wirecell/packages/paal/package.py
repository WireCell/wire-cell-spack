from spack.package import *
#from spack.pkg.builtin.boost import Boost

class Paal(Package):
    """
    Upstream blurb: A header-only, generic library consisting of
    approximation algorithms, data structures and several complete solutions for
    the various optimization problems.

    Commentary:, PAAL has suffered bitrot over the ages, particularly due to
    depending on "boost" code that never went into boost such as "numeric
    bindings".  Maybe that refers to these:

    https://github.com/uBLAS/numeric_bindings
    https://mathema.tician.de/software/boost-numeric-bindings/

    This package merely copies the header files.  It does not attempt to build
    any of the test code.  Building against all of PAAL is very likely NOT
    POSSIBLE.  Compiler beware.
    """
    homepage = "https://paal.mimuw.edu.pl/"
    ### this git server is unavailable, use mirror.
    # git      = "http://siekiera.mimuw.edu.pl:8082/paal"
    git      = "https://github.com/wirecell/paal.git"
    maintainers = ["bv@bnl.gov"]  # for this file, not paal
    # there are neither branches nor tags or other version identifiers.
    version("2017-01-30",
            commit="e537b58d50e93d4a72709821b9ea413008970c6b")
    version("master", branch="master")

    variant('glpk', default=True,
            description='PAAL is mainly a header only library. '
            'If you use linear programming you must link your executable against glpk.')

    depends_on('boost')
    depends_on('glpk', when='+glpk')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        copy_tree("include/paal", join_path(prefix.include, "paal"))

    
