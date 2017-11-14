from spack import *
import os
class WirecellPrototype(Package):
    """Prototype software prior to porting into production Wire Cell Toolkit"""

    homepage = "http://bnlif.github.io/wire-cell-docs/"
    #url = "http://wirecell.github.io"

    version('dev', git="https://github.com/BNLIF/wire-cell.git", submodules=True)

    depends_on("eigen@3.3.4")
    depends_on("fftw")
    # match what is listed in wire-cell-build/wscript
    depends_on("boost+graph+iostreams+filesystem+system+thread+program_options@1.59.0")
    depends_on("root@6:")

    def install(self, spec, prefix):

        cfg = "./waf-tools/waf -v -v"
        cfg += " --prefix=%s" % prefix
        cfg += " --boost-mt"
        cfg += " --boost-libs=%s/lib --boost-includes=%s/include" % \
               (spec["boost"].prefix, spec["boost"].prefix)
        cfg += " --with-root=%s" % spec["root"].prefix
        cfg += " --with-fftw=%s" % spec["fftw"].prefix
        cfg += " --with-eigen=%s" % spec["eigen"].prefix


        cfg += " configure"
        python(*cfg.split())
        python("./waf-tools/waf")
        python("./waf-tools/waf", "install")
        return
