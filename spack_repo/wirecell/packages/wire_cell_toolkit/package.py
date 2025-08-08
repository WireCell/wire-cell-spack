# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.build_systems.cuda import CudaPackage

class WireCellToolkit(Package, CudaPackage):
    """Toolkit for Liquid Argon TPC Reconstruction and Visualization ."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://wirecell.github.io/"
    url      = "https://github.com/WireCell/wire-cell-toolkit/archive/refs/tags/0.23.0.tar.gz"
    git      = "https://github.com/WireCell/wire-cell-toolkit.git"

    license("LGPLv3")

    maintainers = ['brettviren']

    version("master", branch="master")
    version("0.30.5", sha256="f665adf8e75af2ea26176acdae56816db6c1af2ecc86c405c49ab43c6a25e0b2")
    version("0.30.4", sha256="5971364fb1a9b4c52abaeb563c8cc8742c912d6c7c57948de0cb76acd202127b")
    version("0.30.3", sha256="cc95044a9de15cab33992084de94e07716a5c14cf2d3486b993c6ef6bad57027")
    version("0.30.2", sha256="51cf692a9687e3124439ce824597c47e8dea38d7178161e3717602c330d74dc2")
    version("0.30.1", sha256="cefef542978a1a10360e0b90532cde72a67763c2d2d3e8e1b39873ea61b36f45")
    version("0.30.0", sha256="e5a5860145a821ce11d3040d71f7fb2bbfd3776820cd3808fd0cbaf33b401700")
    version("0.29.5", sha256="2a16ae4b4e69bb570d79881f32ceb4868d2a9a16699419dd097765d45da06d03")
    version("0.29.4", sha256="b2dcadc73b0945adbedf8fcaa0c81e0d0c400314514ae399a79b97e45d149415")
    version("0.29.3", sha256="c8c9319cd5abe72db5bb9d5799b5463af3e996a551e17db10fd56281a36e7387")
    version("0.29.2", sha256="7ca719da56d89dbe9ebcbb5755bbce99719a8cababb99aea8e24502f27c95e25")
    version("0.28.0", sha256="62f07ad8bf726ef8aaec428a84cae0ca61ca7b33d5c58f35d2c056f342fdc22c")
    version("0.27.1", sha256="a8410a9e0524570e811f5cca2ea9fc636e48c048a5e67c5cee567b935515e176")
    version("0.27.0", sha256="c4d1dc438b685bc54004425922f9435d8cb7f928a6b080b910cff021392571b2")
    version("0.26.0", sha256="8ad495ef1fb8ca94ee02d77ab9b3873b278bfdce87fc3c2d4dccb8afb8aef41a")
    version("0.25.3", sha256="e92b39335bc3faa1548db95a17fac5462363b4b9b636aaa427044e4a9b51d194")
    version("0.25.2", sha256="aac849da29092d3397f0130f45c499703496188ad74bd347a3bd154fe23f245d")
    version("0.25.1", sha256="c236758a70fd459824f2f769b1e4e146e8f75965833a5aa8a81f0cf08044f9d6")
    version("0.24.3", sha256="040d819a3a81b953a42c8b4bb898acf6978cee45beea0361a2f3cdb602a6028c")
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
    variant('torch', default=False,
            description='Add support for libtorch')
    variant('cuda', default=False,
            description='Add support for CUDA')
    variant('emacs', default=False,
            description='Add support for Emacs for documentation building')

    # new requirements for compilers-as-nodes
    depends_on('c', type=('build',))
    depends_on('cxx', type=('build',))

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

    # used to build documentation.
    depends_on('emacs', when='+emacs')

    depends_on('py-torch~cuda', when='+torch ~cuda')
    # Apparently must exhaustively forward all compute capability versions.
    # This follows how the ams package does things.
    with when("+cuda"):
        depends_on('cuda')
        with when("+torch"):
            depends_on("py-torch+cuda")
            for cc in CudaPackage.cuda_arch_values:
                depends_on(f"py-torch +cuda cuda_arch={cc}",
                           when=f"cuda_arch={cc}")


    # Suggested:

    depends_on('tbb', when='+tbb')


    # Optional:

    # ROOT is needed for wire-cell-toolkit/root
    # Turn off opengl as it brings in an entire copy of llvm (in addition to
    # llvm internal to root) and one which breaks spack environments based on GCC builds.
    depends_on('root @6.28.04: ~opengl cxxstd=17', when='+root')

    depends_on('hdf5 ~mpi+threadsafe', when='+hdf')

    depends_on('h5cpp ~mpi', when='+hdf') # this will go away sometime soon.

    # glpk is needed for wire-cell-toolkit/patrec
    depends_on('glpk', when='+glpk')  

    # TODO: cuda, torch, zmq

    # ----------
    #add version.txt needed when not doing git checkout
    def patch(self):
        with open("version.txt", "w") as version_file:
            version_file.write(f"{self.version}\n")

    def install(self, spec, prefix):

        cfg = ["wcb", "configure", "--prefix="+prefix]

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
        ]

        if 'tbb' in spec:
            cfg += ['--with-tbb=' + spec['tbb'].prefix ]

        # one or the other assured by +/~cppjsonnet?
        if 'jsonnet' in spec:
            jsonnet = 'jsonnet'
            jsonnet_libs = 'jsonnet'
        else:
            jsonnet = 'go-jsonnet'
            jsonnet_libs = 'gojsonnet'
        cfg += [
            "--with-jsonnet=" + spec[jsonnet].prefix,
            "--with-jsonnet-lib=" + spec[jsonnet].prefix.lib,
            "--with-jsonnet-libs=" + jsonnet_libs,
            "--with-jsonnet-include=" + spec[jsonnet].prefix.include,
        ]

        # for now, explicitly turn this off to make sure some random cuda
        # install on the host isn't picked up.
        if spec.satisfies('+cuda'):
            tdir = join_path(self.spec["cuda"].prefix, "targets",
                             f"{self.spec.target.family}-{self.spec.architecture.platform}")
            cfg += [ f'--with-cuda={tdir}' ]
        else:
            cfg += [ "--with-cuda=no" ]

        if spec.satisfies('+torch'):
            cfg.append( "--with-libtorch={0}/lib/python{1}/site-packages/torch".format(
                spec['py-torch'].prefix, spec['python'].version.up_to(2)) )

        else:
            cfg.append( "--with-libtorch=no" )

        # The --notests flag is vestigial in more recent versions but doesn't
        # hurt to keep it in order to avoid making version dependency code here.
        # Tests are always built. To actually run them: ./wcb --tests .
        # Developers should be running tests.  Running them during an install
        # does not add much value.
        bld = ["wcb", "--notests"]
        ins = ["wcb", "install"]

        python = which("python")
        python(*cfg)
        python(*bld)
        python(*ins)

    def setup_run_environment(self, env):
        env.prepend_path("WIRECELL_PATH", self.prefix.share.wirecell);

