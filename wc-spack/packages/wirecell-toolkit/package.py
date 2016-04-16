from spack import Package, version, depends_on
import os
class WirecellToolkit(Package):
    """Description"""

    homepage = "http://wirecell.github.io"
    #url = "http://wirecell.github.io"

    version('dev', git="git@github.com:WireCell/wire-cell-build.git")

    depends_on("eigen")
    depends_on("tbb")
    depends_on("boost@1.60.0:")
    depends_on("root@6:")

    def install(self, spec, prefix):
        git = which("git")
        git('submodule','init')
        git('submodule','update')

        # configure("--prefix=%s" % prefix)
        # make()
        # make("install")
        return
