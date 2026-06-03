# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *

class WireCellPrototype(Package):
    """Protype software for Liquid Argon TPC."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://bnlif.github.io/wire-cell-docs/"
    url      = "https://github.com/BNLIF/wire-cell/archive/refs/tags/v00_14_08.tar.gz"
    git      = "https://github.com/BNLIF/wire-cell.git"

    license("LGPLv3")

    maintainers = ['brettviren']

    version("master", branch="master", submodules=True)
    # version("", sha256="", submodules=True)
    version("v00_17_01", tag="v00_17_01", commit="06dea6ed0ab0eed7aa96d26cf3b55dbc3b09b6cd", submodules=True)
    version("v00_14_11", tag="v00_14_11", commit="0543a6e69ac5d02dbd084b6fa2af76bc3e5a788c", submodules=True)
    version("v00_14_08", tag="v00_14_08", commit="d6338d077b4e0004a4c1c74acb5b7af3015c8f35", submodules=True)

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

    # just for build time (for waf/wcb)
    depends_on('python', type=('build',)) 
    depends_on('pkgconfig', type=('build',)) 

    # Required
    depends_on('eigen @3.4.0:')
    depends_on('fftw @3.3.10: ~mpi')

    depends_on('boost @1.80.0: +system+filesystem+graph')
    # fixme: need to propagate cxxstd better
    depends_on('root @6.28.04: +tmva+minuit+python+fftw+spectrum cxxstd=17')
    depends_on('glpk')  

    def install(self, spec, prefix):

        cfg = ["waf-tools/waf", "configure", "--prefix="+prefix]

        # Prior to and including 0.27.1 the C++ std was hard-wired in the
        # wscript.  After finding out that FNALssi folk were forced to grub
        # around in build/c4che/_cache.py to change it, a nicer way was added
        # that can be more easily hooked in to the quasi standard "cxxstd"
        # variant.  
        # if not spec.satisfies("@:0.27.1"):
        #     cfg += ["--cxxstd="+spec.variants["cxxstd"].value]

        cfg += [
            "--boost-mt",
            "--boost-libs=" + spec['boost'].prefix.lib,
            "--boost-includes=" + spec['boost'].prefix.include,
            "--with-eigen=" + spec['eigen'].prefix,
            "--with-glpk=" + spec['glpk'].prefix,
            "--with-glpk-include=" + spec['glpk'].prefix.include,
            "--with-glpk-lib=" + spec['glpk'].prefix.lib,
            "--with-python=" + spec['python'].prefix,
            "--with-python-include=" + spec['python'].headers.directories[0],
            "--with-python-lib=" + spec['python'].prefix.lib,
        ]


        # The --notests flag is vestigial in more recent versions but doesn't
        # hurt to keep it in order to avoid making version dependency code here.
        # Tests are always built. To actually run them: ./wcb --tests .
        # Developers should be running tests.  Running them during an install
        # does not add much value.
        bld = ["waf-tools/waf", "--notests"]
        ins = ["waf-tools/waf", "--notests", "install"]

        python = which("python")
        python(*cfg)
        python(*bld)
        python(*ins)
