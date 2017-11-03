from spack import *
import sys
import os

class Root(Package):
    """ROOT is a data analysis framework."""
    homepage = "https://root.cern.ch"
    url      = "https://root.cern.ch/download/root_v6.08.00.source.tar.gz"

    version('6.10.08', '48f5044e9588d94fb2d79389e48e1d73', preferred=True)
    version('6.08.06', 'bcf0be2df31a317d25694ad2736df268')
    version('6.08.00', '8462a530d27fa5ca7718ea4437632c3c')
    version('6.07.06', '1180254be7ece0f16142b14381b22d68')
    version('6.07.02', '3fb585bf9fa6ce06ca503173c8bee107')
    version('6.06.02', 'e9b8b86838f65b0a78d8d02c66c2ec55')

    if sys.platform == 'darwin': patch('math_uint.patch')

    depends_on('cmake@3.4.3:', type='build')
    depends_on('pkg-config', type='build')
    depends_on('zlib')
    depends_on("freetype")
    depends_on("pcre")
    depends_on('xz')

    # Want to use the same FFTW everywhere.  Also Eigen and wire-cell itself.
    depends_on("fftw")

    depends_on("graphviz",when="+graphviz")
    depends_on("python@2.7:")   # FNAL holds us back
    depends_on("gsl")
    depends_on("libxml2+python")
    depends_on("jpeg")
    depends_on("sqlite")
    depends_on("openssl@1.0.2k")
    depends_on("libpng")

    ## currently wire-cell doesn't focus on its TBB support so leave
    ## it off to keep for lighter weight dependencies.  Turning it on
    ## for wire-cell, it's probably best to build ROOT with it too.
    # depends_on("tbb")

    def install(self, spec, prefix):
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        options = [source_directory]
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        options += self._cmake_args() 
        options += std_cmake_args                                    

        with working_dir(build_directory, create=True):
            cmake(*options)
            make()
            make("install")



    def _cmake_args(self):

        args = [
            '-Dcxx11=ON',
            '-Dcocoa=OFF',
            '-Dbonjour=OFF',
            '-Dx11=ON',
            '-Dopengl=ON',
            '-Dbuiltin_fftw3=OFF',
            '-Dfftw3=ON',       # anyways, it's on by default
            '-Dminuit2=ON',
            ## see above
            #'-Dtbb=ON',
        ]

        if sys.platform == 'darwin':
            args.extend([
                '-Dcastor=OFF',
                '-Drfio=OFF',
                '-Ddcache=OFF',
            ])
            

        return args
                                    

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('ROOTSYS', self.prefix)
        spack_env.set('ROOT_VERSION', 'v{0}'.format(self.version.up_to(1)))
        spack_env.prepend_path('PYTHONPATH', self.prefix.lib)

    def url_for_version(self, version):
        """Handle ROOT's unusual version string."""
        return "https://root.cern.ch/download/root_v%s.source.tar.gz" % version
