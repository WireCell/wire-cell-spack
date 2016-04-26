from spack import *
import os
class WirecellToolkit(Package):
    """Description"""

    homepage = "http://wirecell.github.io"
    #url = "http://wirecell.github.io"

    version('dev', git="https://github.com/WireCell/wire-cell-build.git")

    depends_on("eigen")
    depends_on("tbb")
    depends_on("boost@1.59.0")
    depends_on("root@6:")

    def install(self, spec, prefix):
        bash = which("bash")
        bash("./switch-git-urls")
        git = which("git")
        git('submodule','init')
        git('submodule','update')

        cfg = "wcb -v -v"
        cfg += " --prefix=%s" % prefix
        cfg += " --boost-mt"
        cfg += " --boost-libs=%s/lib --boost-includes=%s/include" % \
               (spec["boost"].prefix, spec["boost"].prefix)
        cfg += " --with-root=%s" % spec["root"].prefix
        cfg += " configure"
        python(*cfg.split())
        python("wcb")
        python("wcb", "install")
        return
