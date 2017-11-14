from spack import *
import os
class WirecellToolkit(Package):
    """Wire Cell Toolkit provides simulation, signal processing and reconstruction for LArTPC"""

    homepage = "http://wirecell.github.io"
    #url = "http://wirecell.github.io"

    version('dev', git="https://github.com/WireCell/wire-cell-build.git", submodules=True)
    version('0.6.2', git="https://github.com/WireCell/wire-cell-build.git", tag="0.6.2", submodules=True)

    depends_on("jsoncpp")
    depends_on("jsonnet")

    depends_on("fftw")
    depends_on("eigen+fftw@3.3.4")


    # Do not currently make use of TBB.  When we get back to this,
    # probably best to build ROOT with TBB support as well.
    # depends_on("tbb")
    depends_on("root@6:")

    # match what is listed in wire-cell-build/wscript
    depends_on("boost+graph+iostreams+filesystem+system+thread+program_options")


    def install(self, spec, prefix):

        cfg = "wcb"
        cfg += " --prefix=%s" % prefix
        cfg += " --boost-mt"
        cfg += " --boost-libs=%s/lib --boost-includes=%s/include" % \
               (spec["boost"].prefix, spec["boost"].prefix)
        cfg += " --with-root=%s" % spec["root"].prefix
        cfg += " --with-eigen=%s" % spec["eigen"].prefix
        cfg += " --with-jsoncpp=%s" % spec["jsoncpp"].prefix
        cfg += " --with-jsonnet=%s" % spec["jsonnet"].prefix
#        cfg += " --with-tbb=%s" % spec["tbb"].prefix
        cfg += " --with-tbb=false" # for now
        cfg += " --with-fftw=%s" % spec["fftw"].prefix


        cfg += " configure"
        python(*cfg.split())
        python("wcb","-vv")
        python("wcb", "install")
        return
