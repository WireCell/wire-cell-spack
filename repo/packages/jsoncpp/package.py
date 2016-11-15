from spack import *
import os
class Jsoncpp(Package):
    """Description"""

    homepage = "https://github.com/open-source-parsers/jsoncpp"
    url = "https://github.com/open-source-parsers/jsoncpp/archive/1.7.2.tar.gz"

    version('1.7.7', '9b51c65c563463220a8cb5fa33d525f8')
    version('1.7.6', 'd0fcb6a5b11e2a3b1edfbfb03c3bc83e')
    version('1.7.5', '2d5877044dca4edaa8d6d5d3b5df4ff5')
    version('1.7.4', '51a6d5f8832d668daf97790ea59c4926')
    version('1.7.3', 'aff6bfb5b81d9a28785429faa45839c5')
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
