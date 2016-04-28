from spack import *
import os
class Jsoncpp(Package):
    """Description"""

    homepage = "https://github.com/open-source-parsers/jsoncpp"
    url = "https://github.com/open-source-parsers/jsoncpp/archive/1.7.2.tar.gz"

    version('1.7.2', '3989402269147d1f853b57c542037536')
    
    depends_on("cmake")

    def install(self, spec, prefix):
        cmake('.',
              '-DBUILD_STATIC_LIBS=OFF',
              '-DBUILD_SHARED_LIBS=ON',
              *std_cmake_args)
        make()
        make("install")
        return
