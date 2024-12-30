# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWirecell(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/WireCell/wire-cell-python"

    # FIXME: ensure the package is not available through PyPI. If it is,
    # re-run `spack create --force` with the PyPI URL.
    url      = 'https://github.com/WireCell/wire-cell-python/archive/refs/tags/0.14.0.tar.gz'

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['brettviren']

    # FIXME: Add proper versions here.
    version('0.14.0', sha256='2ddbfe4ae55f28cba4077691631c6e817c043c5c19e1d292a4ef849987d6270c')

    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    # depends_on('py-pip@X.Y:', type='build')
    # depends_on('py-wheel@X.Y:', type='build')

    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    depends_on('py-setuptools', type='build')
    # depends_on('py-flit-core', type='build')
    # depends_on('py-poetry-core', type='build')

    # FIXME: Add additional dependencies if required.
    # depends_on('py-foo', type=('build', 'run'))
    depends_on('py-click')
    depends_on('py-numpy')
    depends_on('py-matplotlib')
    depends_on('py-networkx')
    #depends_on('py-jsonnet')
    depends_on('py-sqlalchemy')

    def global_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py
        # FIXME: If not needed, delete this function
        options = []
        return options

    def install_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py install
        # FIXME: If not needed, delete this function
        options = []
        return options
