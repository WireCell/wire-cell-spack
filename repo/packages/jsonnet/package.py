from spack import *


class Jsonnet(Package):
    "A data templating language looking like JSON that produces JSON."

    homepage = "http://jsonnet.org"
    url      = "https://github.com/google/jsonnet/archive/v0.9.3.tar.gz"

    version('0.10.0', '5b98029f90296dc16afa98fcada81b78')
    version('0.9.3', '6715f8f08c4de0b65401a5f0b017f55a')
    version('0.9.2', '9332c94fd65ae855d9185cc6479ba022')
    version('0.9.1', '0993ddfdbe8ac1f2ce17f9356d7cfb89')
    version('0.9.0', '8d995831af6a5446b5f6aa008dce6c77')
    version('0.8.9', '385dedac75511a286882148ef70d5cb0')

    # FIXME: Add additional dependencies if required.
    #depends_on('bazel', type='build')

    def install(self, spec, prefix):
        'Install JSonnet'
        # This can use bazel but we fall back to the crude Makefile in order to
        # avoid the dependency on bazel which brings in JDK.
        make()
        make("libjsonnet.so")
        make("libjsonnet++.so")
        mkdirp(prefix.bin)
        install("jsonnet", prefix.bin)
        mkdirp(prefix.lib)
        install("libjsonnet.so", prefix.lib)
        install("libjsonnet++.so", prefix.lib)
        mkdirp(prefix.include)
        install("include/libjsonnet.h", prefix.include)
        install("include/libjsonnet++.h", prefix.include)
        
